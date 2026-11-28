// /ads.txt：AdSense の運営者 ID が入っているときだけ中身を出す（Google が配布している1行の形式）
import { ADS } from '../lib/monetize';
export const GET = () => {
  const pub = ADS.client.replace(/^ca-/, '');
  const body = pub ? `google.com, ${pub}, DIRECT, f08c47fec0942fa0\n` : '';
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
