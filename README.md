# TOC_project
my TOC project

我做的是可以詢問最近星座運勢的聊天機器人
概念很簡單
就是去parse星座運勢的網頁
然後根據使用者的輸入來進行相對應的回答

例如輸入:
```
我想知道明天金牛座的運勢
```
就會列出明天金牛座的運勢
輸出結果如下:

```
明日金牛座解析
整體運勢★★☆☆☆：公眾場合少說話，眾人談論的八卦話題少摻和進去，易惹是非。在外玩樂要早點回家，否則易引起家人的不滿，聽家人埋怨的話自己也會不太舒服。對金錢的花費要有所節制，不然荷包空空會後悔莫及。
愛情運勢★☆☆☆☆：亂七八糟的桃花運，少碰為妙，惹來一身腥就不好了。
事業運勢★★☆☆☆：顯得衝動易怒，易因工作上的事務而與他人惡語相向，職場人際關係易變得緊張。
財運運勢★★☆☆☆：外出少帶錢，以免為錢傷神。
```

也支援英文輸入，例如輸入:
```
The luck of Gemini of this Month
```

輸出結果如下:
```
本月雙子座解析
整體運勢★★★☆☆：本月總運平平。單身者容易因為粗心大意而錯過身邊的幸福，有伴侶者要避免想得太多而自尋煩惱；工作壓力增大，要學會放鬆；財運佳，投資收益高。
愛情運勢★★☆☆☆：
單身者：桃花運有下滑趨勢，有緣無分的情況時有發生。月初能夠在職場上遇到心動對象，只可惜對方已有意中人，對你的示好避之不及。下半月有朋友會給你介紹異性認識，年齡方面卻不太合適，做朋友的機會比做戀人的機會高很多。
戀愛者：有伴侶者忙於工作，對晉陞的渴望借用了不少對愛情的熱情，不免忽略了對方的感受，容易引起對方往不好的方向猜想。熱衷事業，也要兼顧感情才是，再忙也要抽點時間與對方溝通交流，感情需要時間與精力來用心經營。
事業運勢★★★☆☆：
上班族：本月求職者會遇到較為激烈的競爭，那種門檻較高的大公司還是繞道而行為佳，以免打擊到自己的自信心。在職人員有陪同老闆出差的機會，是擴展人脈的好機會，得體的著裝和禮貌的言語都能為你增加好運。
學生：學生族的課外補習效果顯著，只要老師一點點提示，就能運用自己的超強邏輯思維解決難題。下半月的班會討論活動可積極參與，能從與同學的交流互動中有效提升口才能力。
財運運勢★★★★☆：財運不錯，適合做一些期限短，風險偏高，但收益較大的投資，相信自己的第六感會給你帶來財富的增值。不動產的購置可以提上議程，多參考朋友的建議和長輩的意見，所購產業升值空間將會很大。
```

然後不曉得為什麼我的電腦裝不了pygraphviz
所以產生不了FSM的圖....
