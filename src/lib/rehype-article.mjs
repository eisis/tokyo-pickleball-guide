// 記事の本文（Markdown）を、サイト用の見た目に変える小さな仕組み。追加のライブラリは使わない。
//
// 1. ボックス：引用（>）の1行目に [!POINT] などを書くと、色つきの箱になる
//      > [!POINT]
//      > ここに大事なことを書く
//    種類：POINT（ポイント）/ TIP（ワンポイント）/ CAUTION（注意）/ NOTE（メモ）
// 2. 写真だけの段落は、写真の説明（![ここ](...)）を下に小さく表示する
// 3. 表は横にスクロールできる枠で包む（スマホではみ出さないように）

const BOXES = {
  POINT: 'ポイント',
  TIP: 'ワンポイント',
  CAUTION: '注意',
  NOTE: 'メモ',
};

const el = (tagName, properties, children) => ({ type: 'element', tagName, properties, children });
const isBlank = (n) => n.type === 'text' && !n.value.trim();

function transform(node) {
  if (!node.children) return;
  node.children = node.children.map((child) => {
    if (child.type !== 'element') return child;

    // 1. ボックス
    if (child.tagName === 'blockquote') {
      const firstP = child.children.find((c) => c.type === 'element' && c.tagName === 'p');
      const firstText = firstP?.children?.[0];
      const m = firstText?.type === 'text' && firstText.value.match(/^\s*\[!(POINT|TIP|CAUTION|NOTE)\]\s*/);
      if (m) {
        const kind = m[1];
        firstText.value = firstText.value.slice(m[0].length);
        if (firstP.children.every(isBlank)) child.children = child.children.filter((c) => c !== firstP);
        transform(child);
        return el('aside', { className: ['callout', `callout-${kind.toLowerCase()}`] }, [
          el('p', { className: ['callout-label'] }, [{ type: 'text', value: BOXES[kind] }]),
          ...child.children,
        ]);
      }
    }

    // 2. 写真だけの段落 → 説明つきの写真
    if (child.tagName === 'p') {
      const parts = child.children.filter((c) => !isBlank(c));
      if (parts.length === 1 && parts[0].type === 'element' && parts[0].tagName === 'img') {
        const img = parts[0];
        img.properties.loading = 'lazy';
        const alt = img.properties.alt;
        return el('figure', { className: ['photo'] }, alt ? [img, el('figcaption', {}, [{ type: 'text', value: alt }])] : [img]);
      }
    }

    // 3. 表
    if (child.tagName === 'table') return el('div', { className: ['table-wrap'] }, [child]);

    transform(child);
    return child;
  });
}

export default function rehypeArticle() {
  return (tree) => transform(tree);
}
