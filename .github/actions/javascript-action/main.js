const { installDependencies } = require('./setup');

async function run() {
    try {
        await installDependencies();

        // Now that the dependencies are installed, you can require them:
        const core = require('@actions/core');

        const name = core.getInput('name', { required: true })
        let age = core.getInput('age', { required: true })


        core.notice(`Hello ${name}, you are ${age} ${parseInt(age) !== 1 ? 'years' : 'year'} old!`);
    } catch (error) {
        console.error(`Failed: ${error}`);
    }
}

run();
