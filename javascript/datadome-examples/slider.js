import { Salamoonder } from 'salamoonder-js';

const URL = 'https://example.com/';
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36';
const PROXY = 'http://user:pass@ip:port';
const API_KEY = 'sr-YOUR-KEY';

async function main() {
    const client = new Salamoonder(API_KEY);

    const response = await client.get(URL, {
        headers: { 'User-Agent': USER_AGENT },
        proxy: PROXY,
        impersonate: 'chrome133a',
    });

    const ddCookie = response.cookies.get('datadome');
    if (!ddCookie) {
        console.error('No DataDome cookie found');
        process.exit(1);
    }

    const constructedUrl = client.datadome.parseSliderUrl(response.text, ddCookie, URL);

    const taskId = await client.task.createTask('DataDomeSliderSolver', {
        captcha_url: constructedUrl,
        user_agent: USER_AGENT,
        country_code: 'us',
    });

    const result = await client.task.getTaskResult(taskId);

    if (!result.cookie) {
        console.error('Failed to solve:', result);
        process.exit(1);
    }

    const solvedCookie = result.cookie.split('datadome=')[1].split(';')[0];

    client.session.cookies.set('datadome', solvedCookie, '.example.com', '/');

    const verify = await client.get(URL, {
        headers: { 'User-Agent': USER_AGENT },
        impersonate: 'chrome133a',
    });

    if (verify.statusCode === 200) {
        console.log('Successfully bypassed DD Slider.');
    } else {
        console.error('Bypass failed');
    }
}

main();