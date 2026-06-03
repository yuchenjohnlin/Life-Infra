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
		>  >So I was thinking of using a migrate skill or something, but Claude and Codex said not to. I think it is inevitable but yeah... don't need to over complicate for now. So the current solution is to use a migrate.py script to work on fix the metadata of the files. 
		>  >Another note is the separation of the metadata and the content of the file. This is kind of like a structure in my "Obsidian App" lol, which is why I think that skill can do the schema understanding and migration. Anyways refer to the Migration-Issue for this part.

	4. UI implementation 
		1. First come up with two .base files for Digest and Raw. What are the metadata shown in this interface ? mostly the video's metadata, 

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
		
---
# Migration 

1. About the filename and schema drift, you can see that after I made some changes in the filename and metadata of the template of the digest skill, parts in the extract skill wasn't updated

2. As for the output digest file not matching the template, this is also a drift iissue where I updated the template but the files in the result folders are not updated. THe thing is that I thought we can just rerun it ? but then I found that it's not really worth rerunning because these are actually just "metadata" that don't actually effect the digest and the transcript content. Just some file formats and metadata.

Not to mention doing frontmatter updates after I have already ran 100s of videos, I wouldn't be able to run through every input again.

In view of the above issue, can you give me some advice as a senior software engineer ? Should we write a drift skill ? I can actually just let you change the frontmatter for me though, but I am not sure if this situation is common or not.

I also made a new file @Learn/Dev/05-25 Workflow & Structure Design/2026-05-27 Initial-Implementation/Discussion.md regarding the UI design and workflow issues.

So I have already fixed the filename, metadatas in the skills as well as the consistency between then. However, I found that this metadata and migration is inevitable, so I am thinking of adding schema-version fields to the template metadata. In view of the fact that metadata can have layers (like in object oriented programming you can inherit) same in relation databases where you can actually point to other schemas to add fields, I have the several thoughts. 

1. separate the metadata (frontmatter of the template) from the template's content part. Right now, the metadata and content is in the same template file. I am totally fine with this, but it might be easier to look and present if the metadata or schema was in another schema file with the version name, where the template would just have to kind of import the schema file.
    
2. Another reason is that, the schemas are the ones that change more often compared to the content, and this kind of change shouldn't trigger rerunning. Separating them and then changing them to have different versions of schemas would actually be easier to put it into the template file without changing something else. 
    
3. When coming up with a updated schema with another version, I guess it might be easier to use this schema file to go through every existing file and make changes ?
    
4. I can write a skill that manages the current schemas ? Where the schemas of each file will be more clear and understandable between each other ?
    
5. I understand this might be over engineer, so I want to ask your advice

--- 
[[2026-06-01-Discussion]]