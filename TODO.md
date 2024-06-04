Business
1. prepare data to valid jsonl
1.5. complete should remove the monitor task - tasks should go into a mode of processed, if they have processed, they will not be monitored and the event will not trigger again
1.6. for fail safe, processing and processed will persist, the user will decide if to use it on not, when the app start it will trigger on all the processed/monitored/complete/ready to retrieve.
1.7 after retrieval, according to user config, the data cannot be retrieved twice, all files will be deleted to remove garbage from openai
2. output retrieved jsonl to valid interface
3. batch result interface
5. test - multiple batches
6. expired batch,
7. partially batch processed
8. persist jobs, resume processing on failover

Tech Debt
1. Better interfaces between boundaries
2. Move monitored_items to a managed object
3. remove all garbage created on openai (files, ... ?)
4. Better developer intefaces

5. general refactor - better code architecture (high/low level details, single responsibility)
6. unit tests
7. documentations
8. fix diagram
