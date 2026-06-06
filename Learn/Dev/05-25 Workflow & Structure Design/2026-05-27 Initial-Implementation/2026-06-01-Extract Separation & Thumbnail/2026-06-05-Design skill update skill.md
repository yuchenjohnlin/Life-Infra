好，我現在做了什麼
目前我把extract skill改完了
我先重申一下extract skill包含著哪一些部份
1. input - url,應該要可以支援multiple urls (batch), 但是不知道會不會有ip block問題
2. template - output format of the skill
	1. includes a schema section
	2. raw format for user to see or debug
3. schema - 需要什麼樣的metadata，這個metadata會包含影片本身的資料，影片的原始資料需要處理後才變成給user看的資料，管理影片的資料，其實這些都是資料，但就是我們因為不同需求而需要把這些資料給定義出來。
4. skill本身 - 這個instruction如果沒有定義好，AI會不知道這個skill到底是在做什麼，然後是在什麼樣的情況下使用這個skill
5. 腳本 - 為了讓skill有比較可控制的輸出所以又寫了一個函式來讓skill做使用，這個腳本的話可以有各種的輸入以應對各種情況。

那skill 本身會包含著input, schema, template,script等因為skill需要比較明確的說明這些東西怎麼被使用還有連結來變成一個功能，一個函式，造成說skill, template, script在schema有所變動的時候，也會需要做調整。
這件事情就變得比較麻煩因爲開發的時候都可以很自然而然地增加，因為template, script, schema都是為了有一個更好的結果而產生的，有一個非常強烈的需求。但是到後面因為複雜度上升變得難以管理，而且也會因為過了一段時間而失去對於這個東西的熟悉度。這個熟悉感的消失也是因為複雜度的增加，這裡的複雜度跟前面的不能，不是說本身的這個複雜度，而是指整個結構變得複雜，所以腦袋裡就不會只專注在這一個單元，會在思考這部分的時候就一直跟其他的部分有連結而被分心。這時候就需要明確地分開的定義這個skill或是功能，以及skill本身內部的設計，這樣skill本身某一部分作改動的時候其他部分也才會consistently一起修改，畢竟要達成的目標終歸是一致的。

那我們再多看一個 digest skill的例子來了解一下怎麼去理解一個skill的架構還有怎麼去update一個skill是比較好的。

digest skill
1. input - raw transcript file, includes metadata, and the sections I defined
2. output template - 
	1. includes schema
	2. digest format for user to watch 
3. schema - 針對user想要看到的data
4. skill 本身

好那我現在這上面兩個我會寫得比較詳細是因為我想要可以控制它的輸出讓他能夠產出我所想要的內容，那確實現在功能上是沒問題，因為我就是從功能開始開發的。但是現在整個flow還有function的定義上，卻覺得缺了一些東西，因為一開始沒有遇到一些現在的問題。不過我覺得殊途同歸，就是說我可能一開始著重workflow,development cycle但是有可能到後面也會遇到function, skill的產出跟想像的不一樣。那只要想辦法去解決到後面都是我們目標的不同。Anyways,
我現在發覺我讓skill的寫法有很多種，然後因為我的介面是以Obsidian為主，也會有需要metadata這樣的需求。
其實我就是想要寫一個可以幫忙update skill的skill，ㄟ...我先言歸正傳好了，我又被聊走了。

目標：
最原始的目標：給予一個input file with url，要生成一個digest。
在開發過之後：分成了extract擷取影片資訊，和digest整理統整資料並輸出。我也懶得去想這到底是不是最好的方法反整先這樣
現在的情況：
extract digest有明確的功能，是可以重複使用的skill，但是現在缺一個input是url file，然候在有extract和digest的結果之後去判斷要怎麼做的function，這個function的話一定要輸出一個.digest file(所以這部分就有點麻煩，因為好像輸出的這個功能有點被重複了 (變成這個skill會因為digest的行為而要擦屁股的感覺，會有點dependent，dependent有關係嗎)？
因為digest如果沒有raw file的話好像就不會產生一個digest file)但是只要不會有沒有產生raw file的情況就好了啊，那因為現在也已經有那些error, status metadata了，所以input一定會有raw file，那就也會依訂有digest只是裡面的content metadata會顯示問題到底是什麼。
萬歲！這樣的話就不用再去考慮input沒有raw file但是因為UI的關係所以需要有digest file的情況了。確實啊，只要一定有raw file就不會有問題了，我真是蠢蛋。好，那下一個問題就是input file裡面的url在做完這個process 之後，那個url要繼續存在file裡面嗎？
那以上這個方式我也就不用多寫一個skill，我就可以用Claude.md就可以。

那就可以回到我開發的過程中遇到的那些問題。
1. 我遇到問題然後修改了skill，然後digest, extract這兩個skill需要consistent的update，但是我自己是感覺AI可能自己不會發覺（至少他上次改了python腳本，也改了template但就是沒有改skill，啊我也給忘了，是後面想起來跟他說）所以skill可能要寫說有部分做修改的話，那skill就也要做修改。我是不知道現在AI是不是其實夠強，所以其實我不講他也應該可以意識到，或是他那時候沒有意識到是因為context focus在schema上面，然後其實skill跟schema的連結可能比較不那麼的深。我其實是想知道有這樣一個skill是不是真的會又正的效果。
2. 那如果skill本身比較不複雜就不會有這樣的問題，但是因為Obsidian的metadata, template(也就是我的UI)，導致我勢必會有這樣的問題，因此我也判斷這樣的skill勢必是存在的 - if agreed then action
3. 那要設計這個skill的話就要想一下這是一個只有update skill的skill還是他是一個也會create skill 的skill，因為我元本就有一個 Skill Authoring 的folder因為我知道我會創建更多的skill，然後那時候也在想要怎麼樣寫一個skill會是比較好的。所以create skill & update是需要分開的嗎？另一個問題是這個開發或使用skill的過程除了create update還會有之外的東西嗎？
不過為了能解決現在的問題我們可以先處理一下這個skill update的部分，但是要再討論一下，因為還有所謂的schema migration的部分，也有在想是不是也可以是一個skill，所以要區分一下他們的responsibility還有我到底想要達成什麼樣的，什麼樣是更好的。

skill 設計：
