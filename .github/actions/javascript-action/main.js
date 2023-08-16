const fs = require('fs')
const setup = require('./setup');

async function run() {
    try {
        await setup.installDependencies();

        // Now that the dependencies are installed, you can require them:
        const core = require('@actions/core');
        const exec = require('@actions/exec');

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
          --only-summary
        `;

        let output = '';
        const options = {
            listeners: {
                stdout: (data) => {
                    output += data.toString();
                }
            }
        };

        await exec.exec('bash', ['-c', locustCommands])

        // Extract JSON from the output
        const jsonStart = output.indexOf('[');
        const jsonEnd = output.lastIndexOf(']') + 1;

        if (jsonStart !== -1 && jsonEnd !== -1) {
            const jsonOutput = output.slice(jsonStart, jsonEnd);
            const jsonFilePath = `${jsonDir}/${currTime}.json`;
            fs.writeFileSync(jsonFilePath, jsonOutput, 'utf8');
        }

        // Set GITHUB_OUTPUTS
        core.setOutput("JSON_DIR", jsonDir)
        core.setOutput("CURR_TIME", currTime)

        // Clean up JSON
        const jsonFilePath = `${jsonDir}/${currTime}.json`;
        if (jsonStart !== -1 && jsonEnd !== -1) {
            const jsonOutput = output.slice(jsonStart, jsonEnd);
            fs.writeFileSync(jsonFilePath, jsonOutput, 'utf8');

            // Validate and clean JSON if necessary
            let rawData = fs.readFileSync(jsonFilePath, 'utf8');
            let jsonCleaned = false;

            try {
                JSON.parse(rawData);
                console.log("JSON is valid.");
                core.setOutput("json-cleaned", "true");
            } catch (error) {
                console.log("Invalid JSON detected!");

                // Attempt cleanup: Remove the last line and check again
                const lines = rawData.split('\n');
                lines.pop();
                rawData = lines.join('\n');
                fs.writeFileSync(jsonFilePath, rawData, 'utf8');

                try {
                    JSON.parse(rawData);
                    console.log("JSON is valid after cleanup.");
                    jsonCleaned = true;
                    core.setOutput("json-cleaned", "true");
                } catch (error) {
                    console.error("JSON still invalid after cleanup!");
                    core.setOutput("json-cleaned", "false");
                    core.setFailed("Invalid JSON data.");
                }
            }

            // Format the JSON for readability if it was cleaned or originally valid
            if (jsonCleaned || core.getInput("json-cleaned") === "true") {
                const parsedData = JSON.parse(rawData);
                const formattedJson = JSON.stringify(parsedData, null, 4); // 4 spaces indentation
                fs.writeFileSync(jsonFilePath, formattedJson, 'utf8');
            }
        }

    } catch (error) {
        console.error(`Failed: ${error}`);
    }
}

run();


/*

  steps:
    # Run locust test and output results
    - name: Run locust test
      id: locust-runner
      shell: bash
      run: |
        source .venv/bin/activate
        CURR_TIME=$(date +%Y-%m-%d_%Hh-%Mm-%Ss)
        LOG_DIR="./logfiles"
        HTML_DIR="./htmlfiles"
        CSV_DIR="./csvfiles/$CURR_TIME"
        JSON_DIR="./jsonfiles/$CURR_TIME"

        mkdir -p $LOG_DIR $HTML_DIR $CSV_DIR $JSON_DIR

        locust \
          -f ${{ inputs.locustfile }} \
          --users ${{ inputs.users }} \
          --spawn-rate ${{ inputs.spawn-rate }} \
          --run-time ${{ inputs.run-time }} \
          --headless \
          --logfile $LOG_DIR/$(echo $CURR_TIME)_mylog.log --loglevel INFO \
          --html $HTML_DIR/$(echo $CURR_TIME)_myhtml.html \
          --csv $CSV_DIR/$(echo $CURR_TIME) --csv-full-history \
          --json \
          --exit-code-on-error 1 \
          --only-summary | awk '/\[/{flag=1} flag; /\]/{flag=0; print}' > $JSON_DIR/$(echo $CURR_TIME).json

        echo "JSON_DIR=$JSON_DIR" >> $GITHUB_OUTPUT
        echo "CURR_TIME=$CURR_TIME" >> $GITHUB_OUTPUT

        unset CURR_TIME LOG_DIR HTML_DIR CSV_DIR JSON_DIR

    # Clean JSON Data
    - name: Clean locust output JSON data
      id: json-cleaner
      shell: bash
      run: |
        source .venv/bin/activate
        BLUE="\033[34m"
        RESET="\033[0m"
        JSON_DIR="${{ steps.locust-runner.outputs.JSON_DIR }}"
        CURR_TIME="${{ steps.locust-runner.outputs.CURR_TIME }}"

        if ! jq '.' $JSON_DIR/$(echo $CURR_TIME).json 2>/dev/null; then
          echo -e "${BLUE}Invalid JSON detected!${RESET}"
          sed -i '$d' $JSON_DIR/$(echo $CURR_TIME).json
          if ! jq '.' $JSON_DIR/$(echo $CURR_TIME).json 2>/dev/null; then
            echo -e "${BLUE}JSON still invalid!${RESET}"
            echo "json-cleaned='false'" >> $GITHUB_OUTPUT
            exit 1
          else
            echo -e "${BLUE}JSON is valid.${RESET}"
            echo "json-cleaned='true'" >> $GITHUB_OUTPUT
          fi
        else
          echo -e "${BLUE}JSON is valid.${RESET}"
          echo "json-cleaned='true'" >> $GITHUB_OUTPUT
        fi

        unset BLUE RESET JSON_DIR

      continue-on-error: true

 */