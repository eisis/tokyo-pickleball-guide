// 広告・アフィリエイトの設定。ID は Vercel の環境変数で入れる（コードには書かない）。
// どれかが空のあいだは、その広告・リンクは一切表示されない（審査前でもサイトの見た目は変わらない）
//   PUBLIC_ADSENSE_CLIENT        … AdSense のサイト運営者 ID（ca-pub-xxxxxxxxxxxxxxxx）
//   PUBLIC_ADSENSE_SLOT_ARTICLE  … 記事の下に出す広告ユニットの ID（数字）
//   PUBLIC_AMAZON_TAG            … Amazon アソシエイトのトラッキング ID（xxxx-22）
//   PUBLIC_RAKUTEN_AFID          … 楽天アフィリエイト ID（xxxxxxxx.xxxxxxxx.xxxxxxxx.xxxxxxxx）
const env = import.meta.env;
const v = (k: string) => String(env[k] ?? '').trim();

export const ADS = {
  client: v('PUBLIC_ADSENSE_CLIENT'),
  articleSlot: v('PUBLIC_ADSENSE_SLOT_ARTICLE'),
};
export const AFF = {
  amazonTag: v('PUBLIC_AMAZON_TAG'),
  rakutenId: v('PUBLIC_RAKUTEN_AFID'),
};
export const adsEnabled = Boolean(ADS.client && ADS.articleSlot);
export const affiliateEnabled = Boolean(AFF.amazonTag || AFF.rakutenId);

/** Amazon の検索結果へのリンク（特定の商品を推さず、選ぶのは読者に任せる） */
export const amazonSearchUrl = (keyword: string) =>
  AFF.amazonTag ? `https://www.amazon.co.jp/s?k=${encodeURIComponent(keyword)}&tag=${encodeURIComponent(AFF.amazonTag)}` : '';

/** 楽天市場の検索結果へのリンク（楽天アフィリエイトのリンク形式） */
export const rakutenSearchUrl = (keyword: string) =>
  AFF.rakutenId
    ? `https://hb.afl.rakuten.co.jp/hgc/${AFF.rakutenId}/?pc=${encodeURIComponent(`https://search.rakuten.co.jp/search/mall/${encodeURIComponent(keyword)}/`)}`
    : '';
