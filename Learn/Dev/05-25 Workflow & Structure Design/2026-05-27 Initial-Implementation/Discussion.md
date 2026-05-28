Following from the messier [[2026-05-25-Discussion]], this file contains a clearer goal of what to be done. 

1. UI Design 
	1. inbox file serves as a queue and user input.
	2. Interface for raw transcript 
	3. Interface for digest 


		> [!note]+ Design Decision
		> Whether just use one interface or two ?  Having one unified interface would seems better "maybe?", since the metadata for digest and transcript kind of overlap and it would be easier to navigate. 
		> However, another question for this is, would I actually look at the transcript file ? Maybe not, and the reason for including the transcript file in the view is just me imagining that knowing the transcript file can let us understand if it's processed or not. Now thinking about it, maybe the 2 .base is not needed. We can just have one .base file which uses the metadata of that in the digests, with each linking back to its raw transcript and metadata file. 

		> [!question]+ Issues
		> 1. Metadata of the transcript and digest is not defined well enough. Add status of the video and define the possible status. 
		> 	Add status for both files. Add viewed_state for digest
		> 2. Filename of the transcript and digest is not defined in the skill, and after changing the skill, make sure the filenames and metadata in the skill is consistent. 
		> 3. After the above changes were made to the skill, the previous test files should also have corresponding changes, but they didn't because they need to be updated. I was thinking maybe just rerun it, but what we're updating were just the metadata, not the content or the transcript. Let alone the fact that yt actually has rate limits so rerunning is not a good option. The metadata for the video also changes with the time, 
		>  >[!note]- How should we do the drift ? AI ? 
		>  >

## Mental Model 
The mental model or design philosophy is kind of changed here. Previously, I had the structure of **" First get the transcript sources. Then according to the sources go to the next step."** 
This emphasizes the source a lot, making it like the main character?, kind of like a pipeline. But after considering the UI that faces the user, an universal interface that tells the user what happens is needed, which is the .base file where images and title is shown to the user to click and go into the video. 
The UI is emphasized, being the main character, so everything surrounds the UI rather than the source. The UI doesn't care if what happened, you just have to tell me the status so that it can let the user know. Previously, if we didn't have a source, then we wouldn't have a transcript file (I am actually not sure, but in my mind I had that in mind). 
I also figured that the components can be listed as follows, 
1. metadata of transcript source 
2. metadata of digest (for user) 
3. common metadata for video 
4. transcript content and transcript format 
5. digest content and digest format. 
		
