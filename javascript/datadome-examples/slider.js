import { Salamoonder } from 'salamoonder-js';

const URL = 'https://example.com/';
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36';
const PROXY = 'http://user:pass@ip:port';
const API_KEY = 'sr-YOUR-KEY';

const HEADERS = {
    'User-Agent': USER_AGENT,
    'sec-ch-ua': '"Google Chrome";v="146", "Not-A.Brand";v="8", "Chromium";v="146"',
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

    const sliderChallenge = await client.datadome.getSliderChallenge(
        response.text,
        ddCookie,
        URL,
        { user_agent: USER_AGENT }
    );

    const taskId = await client.task.createTask('DataDomeSliderSolver', {
        captcha_url: sliderChallenge.captcha_url,
        challenge_page: sliderChallenge.challenge_page,
        user_agent: USER_AGENT,
    });

    const result = await client.task.getTaskResult(taskId);

    if (!result.url) {
        console.error('Failed to solve:', result);
        process.exit(1);
    }

    const cookieResponse = await client.get(result.url, {
        headers: HEADERS,
        proxy: PROXY,
        impersonate: 'chrome133a',
    });

    console.log(cookieResponse.text);
}

main();