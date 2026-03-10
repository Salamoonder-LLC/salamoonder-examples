import { Salamoonder } from 'salamoonder-js';

const URL = 'https://yourdomain.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fp?x-kpsdk-v=j-1.2.170';
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36';
const PROXY = 'http://user:pass@ip:port';
const API_KEY = 'sr-YOUR-KEY';

async function main() {
    const client = new Salamoonder(API_KEY);

    const scriptData = await client.kasada.parseKasadaScript(URL, USER_AGENT, PROXY);
    if (!scriptData) throw new Error('Failed to extract Kasada script');

    const taskId = await client.task.createTask('KasadaPayloadSolver', {
        url: 'https://yourdomain.com',
        script_url: scriptData.script_url,
        script_content: scriptData.script_content,
    });

    const result = await client.task.getTaskResult(taskId, 5);

    const postSolution = await client.kasada.postPayload(
        'https://yourdomain.com',
        result,
        USER_AGENT,
        PROXY,
        false
    );

    console.log(JSON.stringify(postSolution, null, 2));
}

main();