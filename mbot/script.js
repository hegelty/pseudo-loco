importClass(org.jsoup.Jsoup);


function response(room, msg, sender, isGroupChat, replier, imageDB, packageName) {
    if(msg.split(' ')[0] == "!멘션") {
        let target = msg.split(' ')[1];
        if(target[0] == '@') {
            Jsoup.connect("http://172.30.104.212:8000/mention")\
                .method(Method.POST)
                .data("room", room)
                .data("target", target)
                .data("message", "pseudo-loco test")
                .ignoreContentType(true)
                .execute();
        }
    }
}