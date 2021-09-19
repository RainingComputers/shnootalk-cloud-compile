# shnootalk-cloud-compile

Backend and infrastructure to compile and execute ShnooTalk programs on the cloud.
Primary use case is for users to try the language in the browser.

The project is made up of two sub-projects, the job and the server. The server
has endpoints to dispatch programs (start compile and run jobs on a kubernetes cluster)
and query status of execution. The job does the actual compilation and execution.

Both the server and the job use MongoDB to keep track of the execution status.