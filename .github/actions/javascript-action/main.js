const { installDependencies } = require('./setup');

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
