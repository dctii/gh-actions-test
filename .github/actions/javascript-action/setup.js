const { exec} = require('child_process');

exec(
    'npm install @actions/core @actions/github @actions/exec',
    (
        error,
        stdout,
        stderr
    ) => {
    if (error) {
        console.error(`exec error: ${error}`);
        process.exit(1);
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
});

