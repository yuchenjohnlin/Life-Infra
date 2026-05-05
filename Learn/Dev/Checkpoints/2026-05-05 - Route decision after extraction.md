Review current status : 
Previously I have already done research in yt-dlp and youtube-transcript-api. I think I had a decent amount of understanding, but after considering multiple languages and doing more research about them. I now have the full picture. 
Currently, I was considering using bilibili to get the subtitles, to solve the no subtitle issue for Chinese videos. 
But I can also postpone this, and continue to work on the whole flow, and then work more on this later. 
Let's talk about the whole flow and then contemplate about routes I can work on following up at the end : 
This flow is to finish the learning system -> learn from videos -> too much so need AI to filter and summarize beforehand

To learn from videos, 
1. Fetch youtube videos, the current inbox is done manually, haven't automized. Will probably have AI do web search for a targeting topic. 
2. Get metadata of youtube videos, previously worked on Karpathy video from metadata extraction to summarization and rating. I was trying to understand how to design the skills and how to do summarization, and go through 1 video first to work on each step of the flow. 
	- Why didn't I run the process on other videos so that I don't need to rework the extraction part ? 
		  I did run the process on other videos. Most of them worked so I wasn't aware about no-subtitle issues and didn't investigate in detailed information yt-api gets. 
		  At that time the process was still very raw and not refined so I focused on getting good results on 1 video first (Karpathy). 
		  %% This is also a product development decision. Are there any optimization that can be done ? I think this is like a methodology, my method at first is to understand the steps of the whole process and flow, focusing on 1 video. I didn't concern other factors like other languages because I was focusing on English & Chinese videos, which I thought yt-dlp and api was enough. But maybe, I didn't need to go through the whole process at first, and actually came up with a decent benchmark for testing. Because it was after I considered the testset that I found some corner cases and started looking more into the details. %%
	I would run tests on other videos I randomly get online to see how a new version works. They all worked and didn't seem to have any problem so I didn't really focus on them. I focused more on the Karpathy summarization part because it wasn't giving me the content I want so I tried optimizing the summarization skill and process. 
3. While working on summarization of "2": 
   I tried letting AI run the summarization without much prompting, and it turned out better than the summarization I had in the "process-youtube" skill.
	   Two possible reasons things : 
		   1. Putting the summarization in the whole flow makes the summarization worse. ( I didn't "test" it, but had that feeling of putting all steps in one skill results in worse results. I think this makes sense since LLM's context matters a lot, and putting multiple irrelevant steps together I think increases the noise. What I had in mind was that the steps are relevant, since I thought understanding the previous step might help ? But thinking of skills as functions, you can actually just provide input, output for several tasks like summarization. )
		   2. The prompting of the summarization part is bad. This might actually be the main reason given the fact that current LLMs are so powerful such that putting all steps in one skill might not effect the result. 
4. It was then I just thought about the fact that I need a test set or a fixed set of videos to work on. Due to the following thoughts : 
	1. I think there is no way for me to verify if the summarized content is good unless I actually look at the videos. 
	2. I often test on other videos, but I usually just randomly look for more videos, and not actually keeping a record. Having a mindset of, "oh, the more that I run the more that I would win." Yet, I don't even go look into the results because I think it's not good. We'll see if these files can be used as a comparison in the future or not. 
5. Came up with a test set. 
6. Worked from the beginning, starting from metadata extraction. After some research, no auto-generated subtitles can be extracted from Chinese videos. I have to decide if we have to solve this issue or not. 
   One critical concept or goal I bare in mind when designing the extraction process is that the temporary goal is to **get a metadata & subtitle file**. It serves as a record as well as an input to the following workflow.
	1. Try solving the issue
		1. Get subtitles from bilibili - However, there would be subsequent problems
			1. Look for the bilibili url for the youtube video - another searching step 
			2. bilibili needs SESSDATA (login session) to fetch the subtitles - needs to manage the token monthly
			3. Not sure what kind of subtitle format bilibili uses - might need additional effort on the process of getting subtitle (can't just use current process)
			4. Do I actually watch bilibili videos ? I think most of the content there are from america sources.
			   Worthy resources are podcasts where famous or senior engineers share their experience.
		2. Local models that turn audio source into text
			1. Setup DGX Spark server to use good speech models (focusing on Chinese translation not multilingual models like Whisper)
			2. A lot more to understand for this part... - but the amount of work is to just get Chinese subtitles - yeah I think it's not worth doing right now. 
	2. Don't solve the issue for now 
		1. Confirm the extraction process and finish the skill
		2. Design the display format, inbox & what the metadata & subtitle format looks like. 
		3. Test on the test set
7. Then summarization ..........


