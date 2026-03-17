import { Salamoonder } from 'salamoonder-js';

const URL = 'https://example.com/';
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36';
const PROXY = 'http://user:pass@ip:port';
const API_KEY = 'sr-YOUR-KEY';

const HEADERS = {
    'User-Agent': USER_AGENT,
    'sec-ch-ua': '"Google Chrome";v="139", "Not-A.Brand";v="8", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'accept-language': 'en-US,en;q=0.9',
};

async function main() {
    const client = new Salamoonder(API_KEY);

    const response = await client.get(URL, {
        headers: HEADERS,
        proxy: PROXY,
        impersonate: 'chrome133a',
    });

    const ddCookie = response.cookies.get('datadome');
    if (!ddCookie) {
        console.error('No DataDome cookie found');
        process.exit(1);
    }

    const constructedUrl = client.datadome.parseInterstitialUrl(response.text, ddCookie, URL);

    const taskId = await client.task.createTask('DataDomeInterstitialSolver', {
        captcha_url: constructedUrl,
        user_agent: USER_AGENT,
        country_code: 'us',
    });

    const result = await client.task.getTaskResult(taskId);

    if (!result.cookie) {
        console.error('Failed to solve challenge:', result);
        process.exit(1);
    }

    const cookieStr = result.cookie;
    const solvedCookie = cookieStr.includes('datadome=')
        ? cookieStr.split('datadome=')[1].split(';')[0]
        : cookieStr.split(';')[0];

    client.session.cookies.set('datadome', solvedCookie, '.example.com', '/');

    const verify = await client.get(URL, {
        headers: HEADERS,
        proxy: PROXY,
        impersonate: 'chrome133a',
    });

    if (verify.statusCode === 200) {
        console.log(verify.text);
        console.log('Successfully bypassed Interstitial!');
    } else {
        console.error('Bypass failed:', verify.text);
    }
}

main();