const { exec } = require('child_process');

function installDependencies() {
    return new Promise((resolve, reject) => {
        exec('npm install @actions/core @actions/github @actions/exec', (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                reject(error);
                return;
            }
            console.log(`stdout: ${stdout}`);
            if (stderr) {
                console.error(`stderr: ${stderr}`);
            }
            resolve();
        });
    });
}

async function run() {
    try {
        await installDependencies();

        // Now that the dependencies are installed, you can require them:
        const core = require('@actions/core');

        core.notice('Hello from my custom JavaScript Action!');
    } catch (error) {
        console.error(`Failed: ${error}`);
    }
}

run();
