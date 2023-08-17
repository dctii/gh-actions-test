/*
Toolkits: https://github.com/actions/toolkit/blob/master/README.md
npm install \
    @actions/core - inputs, outputs, results, logging, secrets, and variables
    @actions/exec - exec cli tools and process output
    @actions/glob - search for files, matching glob patterns
    @actions/io - disk i/o functions like cp, mv, rmRF, find, etc
    @actions/tool-cache - downloading and caching tools, e.g., setup-* actions
    @actions/github - Octokit client hydrated with the context that the current action is being run in
    @actions/artifact - interact with actions artifacts
    @actions/cache - cache dependencies and build outputs to improve workflow execution time

*/

const fs = require('fs')
const setup = require('./setup');

async function run() {
    try {
        await setup.installDependencies();
    } catch (error) {
        console.error(error)
    }

    const core = require('@actions/core');
    const exec = require('@actions/exec');

    try {
        // Get input values
        const locustfile = core.getInput('locustfile', { required: true })
        const userCount = core.getInput('users', { required: true })
        const spawnRate = core.getInput('spawn-rate', { required: true })
        const runTime = core.getInput('run-time', { required: true })

        // Generate the current time with JavaScript
        const currentDate = new Date();
        const currTime = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()}_${currentDate.getHours()}h-${currentDate.getMinutes()}m-${currentDate.getSeconds()}s`;

        // Define directories using JavaScript
        const logDir = "./logfiles";
        const htmlDir = "./htmlfiles";
        const csvDir = `./csvfiles/${currTime}`;
        const jsonDir = `./jsonfiles/${currTime}`;



        const locustCommands = `
        source .venv/bin/activate
 
        mkdir -p ${logDir} ${htmlDir} ${csvDir} ${jsonDir}

        locust \\
          -f ${locustfile} \\
          --users ${userCount} \\
          --spawn-rate ${spawnRate} \\
          --run-time ${runTime} \\
          --headless \\
          --logfile ${logDir}/${currTime}_mylog.log --loglevel INFO \\
          --html ${htmlDir}/${currTime}_myhtml.html \\
          --csv ${csvDir}/${currTime} --csv-full-history \\
          --json \\
          --exit-code-on-error 1 \\
          --only-summary | awk '/\\[/{flag=1} flag; /\\]/{flag=0; print}' > ${jsonDir}/${currTime}.json
        `;

        core.notice("Initiating locust run.")
        await exec.exec('bash', ['-c', locustCommands])
        core.notice("Locust run finished executing.")

        // Set GITHUB_OUTPUTS
        core.setOutput("JSON_DIR", jsonDir)
        core.setOutput("CURR_TIME", currTime)
        core.notice("Set JSON_DIR and CURR_TIME outputs successfully.")

        const cleanJsonCommands = `
        if ! jq '.' ${jsonDir}/${currTime}.json 2>/dev/null; then
          echo -e "Invalid JSON detected!"
          sed -i '$d' ${jsonDir}/${currTime}.json
          if ! jq '.' ${jsonDir}/${currTime}.json 2>/dev/null; then
            echo -e "JSON still invalid!"
            exit 1
          else
            echo -e "JSON is valid."
          fi
        else
          echo -e "JSON is valid."
        fi
        `

        try {
            await exec.exec('bash', ['-c', cleanJsonCommands]);
            core.notice("JSON cleaned successfully.")
            core.setOutput("json-cleaned", "true");
        } catch (error) {
            core.error("Error in cleaning JSON:", error.message);
            core.setOutput("json-cleaned", "false");
        }

    } catch (error) {
        core.error(`Failed: ${error}`);
    }
}

run();