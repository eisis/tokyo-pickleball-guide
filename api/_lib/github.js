// ============================================================
// GitHub に「承認待ちの変更（プルリクエスト）」を作る
//   申請 → ブランチにファイルを置く → PR を作る → 運営者が Merge すると公開
// 必要な環境変数：GITHUB_SUBMIT_TOKEN（このリポジトリだけの Contents / Pull requests 読み書き権限）
// ============================================================

const REPO = process.env.GITHUB_REPO || 'eisis/tokyo-pickleball-guide';
const BASE = process.env.GITHUB_BASE_BRANCH || 'main';

export const githubReady = () => Boolean(process.env.GITHUB_SUBMIT_TOKEN);

async function gh(path, { method = 'GET', body, allow404 = false } = {}) {
  const r = await fetch(`https://api.github.com/repos/${REPO}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${process.env.GITHUB_SUBMIT_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'pickleball-tokyo-submit',
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (allow404 && r.status === 404) return null;
  if (!r.ok) throw new Error(`github ${method} ${path}: ${r.status} ${(await r.text()).slice(0, 200)}`);
  return r.status === 204 ? null : r.json();
}

/** main にあるファイルの中身（なければ null） */
export async function readFile(path) {
  const j = await gh(`/contents/${encodeURI(path)}?ref=${BASE}`, { allow404: true });
  if (!j) return null;
  return Buffer.from(j.content, 'base64').toString('utf8');
}

export async function fileExists(path) {
  return (await gh(`/contents/${encodeURI(path)}?ref=${BASE}`, { allow404: true })) !== null;
}

/** main にあるフォルダのファイル名一覧（なければ []） */
export async function listDir(path) {
  const j = await gh(`/contents/${encodeURI(path)}?ref=${BASE}`, { allow404: true });
  return Array.isArray(j) ? j.filter((f) => f.type === 'file').map((f) => f.name) : [];
}

/** files から、base の上に積むコミットを作る（ブランチはまだ動かさない） */
async function makeCommit(baseSha, message, files) {
  const baseCommit = await gh(`/git/commits/${baseSha}`);
  const tree = [];
  for (const f of files) {
    const blob = await gh('/git/blobs', {
      method: 'POST',
      body: f.base64 ? { content: f.base64, encoding: 'base64' } : { content: f.content, encoding: 'utf-8' },
    });
    tree.push({ path: f.path, mode: '100644', type: 'blob', sha: blob.sha });
  }
  const newTree = await gh('/git/trees', { method: 'POST', body: { base_tree: baseCommit.tree.sha, tree } });
  return gh('/git/commits', {
    method: 'POST',
    body: { message, tree: newTree.sha, parents: [baseSha], author: { name: 'Pickleball Tokyo 掲載フォーム', email: 'noreply@pickleball-tokyo.com' } },
  });
}

/**
 * 確認なしで main に直接反映する（承認済みの主催者のイベント用）。Vercel が自動で公開する
 * 同時に別の変更が入って失敗したときは、最新の main に積み直して1回だけやり直す
 * 戻り値：{ sha, url }
 */
export async function commitToMain({ message, files }) {
  for (let i = 0; i < 2; i++) {
    const ref = await gh(`/git/ref/heads/${BASE}`);
    const commit = await makeCommit(ref.object.sha, message, files);
    try {
      await gh(`/git/refs/heads/${BASE}`, { method: 'PATCH', body: { sha: commit.sha, force: false } });
      return { sha: commit.sha, url: commit.html_url || `https://github.com/${REPO}/commit/${commit.sha}` };
    } catch (e) {
      if (i === 1) throw e;
    }
  }
}

/**
 * files: [{ path, content(string) } | { path, base64 }]
 * 戻り値：{ number, url }
 */
export async function createPullRequest({ branch, title, body, message, files, labels = [] }) {
  const ref = await gh(`/git/ref/heads/${BASE}`);
  const baseSha = ref.object.sha;
  const baseCommit = await gh(`/git/commits/${baseSha}`);

  const tree = [];
  for (const f of files) {
    const blob = await gh('/git/blobs', {
      method: 'POST',
      body: f.base64 ? { content: f.base64, encoding: 'base64' } : { content: f.content, encoding: 'utf-8' },
    });
    tree.push({ path: f.path, mode: '100644', type: 'blob', sha: blob.sha });
  }
  const newTree = await gh('/git/trees', { method: 'POST', body: { base_tree: baseCommit.tree.sha, tree } });
  const commit = await gh('/git/commits', {
    method: 'POST',
    body: { message, tree: newTree.sha, parents: [baseSha], author: { name: 'Pickleball Tokyo 掲載フォーム', email: 'noreply@pickleball-tokyo.com' } },
  });
  await gh('/git/refs', { method: 'POST', body: { ref: `refs/heads/${branch}`, sha: commit.sha } });
  const pr = await gh('/pulls', { method: 'POST', body: { title, head: branch, base: BASE, body, maintainer_can_modify: true } });
  if (labels.length) {
    try { await gh(`/issues/${pr.number}/labels`, { method: 'POST', body: { labels } }); } catch (e) { console.error('label failed', e.message); }
  }
  return { number: pr.number, url: pr.html_url };
}
