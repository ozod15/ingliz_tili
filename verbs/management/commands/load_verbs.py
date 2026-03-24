from django.core.management.base import BaseCommand
from verbs.models import Verb


class Command(BaseCommand):
    help = 'Load irregular verbs organized by periods with Uzbek translations'

    def handle(self, *args, **options):
        # Organized by periods (common English learning groups)
        verbs_data = [
            # Period 1 - Most Common (20 verbs)
            ("be", "was/were", "been", "/biː/", "bo'lish", "быть", "to be"),
            ("have", "had", "had", "/hæv/", "ega bo'lish", "иметь", "to have"),
            ("do", "did", "done", "/duː/", "qilmoq", "делать", "to do"),
            ("go", "went", "gone", "/ɡəʊ/", "borish", "идти", "to go"),
            ("make", "made", "made", "/meɪk/", "yasamoq", "делать", "to make"),
            ("say", "said", "said", "/seɪ/", "aytmoq", "сказать", "to say"),
            ("get", "got", "got", "/ɡet/", "olmoq", "получить", "to get"),
            ("take", "took", "taken", "/teɪk/", "olmoq", "взять", "to take"),
            ("come", "came", "come", "/kʌm/", "kelmoq", "прийти", "to come"),
            ("see", "saw", "seen", "/siː/", "ko'rmoq", "увидеть", "to see"),
            ("know", "knew", "known", "/nəʊ/", "bilmoq", "знать", "to know"),
            ("think", "thought", "thought", "/θɪŋk/", "o'ylamoq", "думать", "to think"),
            ("give", "gave", "given", "/ɡɪv/", "bermoq", "дать", "to give"),
            ("find", "found", "found", "/faɪnd/", "topmoq", "найти", "to find"),
            ("tell", "told", "told", "/tel/", "aytmoq", "сказать", "to tell"),
            ("become", "became", "become", "/bɪˈkʌm/", "bo'lib qolmoq", "становиться", "to become"),
            ("leave", "left", "left", "/liːv/", "ketmoq", "уйти", "to leave"),
            ("put", "put", "put", "/pʊt/", "qo'ymoq", "положить", "to put"),
            ("keep", "kept", "kept", "/kiːp/", "saqlamoq", "держать", "to keep"),
            ("let", "let", "let", "/let/", "ruxsat berish", "позволить", "to let"),
            
            # Period 2 - Actions (20 verbs)
            ("begin", "began", "begun", "/bɪˈɡɪn/", "boshlash", "начать", "to begin"),
            ("break", "broke", "broken", "/breɪk/", "sindirmoq", "сломать", "to break"),
            ("bring", "brought", "brought", "/brɪŋ/", "keltirmoq", "принести", "to bring"),
            ("build", "built", "built", "/bɪld/", "qurmoq", "построить", "to build"),
            ("buy", "bought", "bought", "/baɪ/", "sotib olmoq", "купить", "to buy"),
            ("catch", "caught", "caught", "/kætʃ/", "ushlash", "поймать", "to catch"),
            ("choose", "chose", "chosen", "/tʃuːz/", "tanlash", "выбрать", "to choose"),
            ("cut", "cut", "cut", "/kʌt/", "kesmoq", "резать", "to cut"),
            ("deal", "dealt", "dealt", "/diːl/", "muomala qilmoq", "иметь дело", "to deal"),
            ("draw", "drew", "drawn", "/drɔː/", "chizmoq", "рисовать", "to draw"),
            ("drink", "drank", "drunk", "/drɪŋk/", "ichmoq", "пить", "to drink"),
            ("drive", "drove", "driven", "/draɪv/", "haydamoq", "вести (машину)", "to drive"),
            ("eat", "ate", "eaten", "/iːt/", "yemoq", "есть", "to eat"),
            ("fall", "fell", "fallen", "/fɔːl/", "tushmoq", "упасть", "to fall"),
            ("feel", "felt", "felt", "/fiːl/", "hiss qilmoq", "чувствовать", "to feel"),
            ("fight", "fought", "fought", "/faɪt/", "jang qilmoq", "бороться", "to fight"),
            ("fly", "flew", "flown", "/flaɪ/", "uchmoq", "летать", "to fly"),
            ("grow", "grew", "grown", "/ɡrəʊ/", "o'smoq", "расти", "to grow"),
            ("hear", "heard", "heard", "/hɪə/", "eshitmoq", "слышать", "to hear"),
            ("hit", "hit", "hit", "/hɪt/", "urmoq", "ударить", "to hit"),
            
            # Period 3 - Movement & Communication (20 verbs)
            ("hold", "held", "held", "/həʊld/", "ushlab turmoq", "держать", "to hold"),
            ("hurt", "hurt", "hurt", "/hɜːt/", "azar yetkazmoq", "повредить", "to hurt"),
            ("learn", "learnt", "learnt", "/lɜːn/", "o'rganmoq", "учить", "to learn"),
            ("lead", "led", "led", "/liːd/", "boshqarmoq", "вести", "to lead"),
            ("lend", "lent", "lent", "/lend/", "qarz berish", "одолжить", "to lend"),
            ("lose", "lost", "lost", "/luːz/", "yo'qotmoq", "потерять", "to lose"),
            ("meet", "met", "met", "/miːt/", "uchrashmoq", "встретить", "to meet"),
            ("pay", "paid", "paid", "/peɪ/", "to'lamoq", "платить", "to pay"),
            ("read", "read", "read", "/riːd/", "o'qimoq", "читать", "to read"),
            ("ride", "rode", "ridden", "/raɪd/", "minmoq", "ехать верхом", "to ride"),
            ("ring", "rang", "rung", "/rɪŋ/", "qichqirmoq", "звонить", "to ring"),
            ("rise", "rose", "risen", "/raɪz/", "ko'tarilmoq", "подниматься", "to rise"),
            ("run", "ran", "run", "/rʌn/", "yugurmoq", "бежать", "to run"),
            ("sell", "sold", "sold", "/sel/", "sotmoq", "продать", "to sell"),
            ("send", "sent", "sent", "/send/", "yubormoq", "отправить", "to send"),
            ("set", "set", "set", "/set/", "o'rnatmoq", "установить", "to set"),
            ("shake", "shook", "shaken", "/ʃeɪk/", "silkitmoq", "трясти", "to shake"),
            ("shine", "shone", "shone", "/ʃaɪn/", "yaltiramoq", "сиять", "to shine"),
            ("shoot", "shot", "shot", "/ʃɒt/", "otmoq", "стрелять", "to shoot"),
            ("show", "showed", "shown", "/ʃəʊ/", "ko'rsatmoq", "показать", "to show"),
            
            # Period 4 - More Common (20 verbs)
            ("shut", "shut", "shut", "/ʃʌt/", "yopmoq", "закрыть", "to shut"),
            ("sing", "sang", "sung", "/sɪŋ/", "qoʻshiq aytmoq", "петь", "to sing"),
            ("sit", "sat", "sat", "/sɪt/", "o'tirmoq", "сидеть", "to sit"),
            ("sleep", "slept", "slept", "/sliːp/", "uxlamoq", "спать", "to sleep"),
            ("speak", "spoke", "spoken", "/spiːk/", "gapirmoq", "говорить", "to speak"),
            ("spend", "spent", "spent", "/spend/", "sarflamoq", "тратить", "to spend"),
            ("stand", "stood", "stood", "/stænd/", "turmoq", "стоять", "to stand"),
            ("steal", "stole", "stolen", "/stiːl/", "o'g'rilamoq", "украсть", "to steal"),
            ("stick", "stuck", "stuck", "/stɪk/", "yopishtirmoq", "приклеить", "to stick"),
            ("strike", "struck", "struck", "/straɪk/", "urmoq", "ударить", "to strike"),
            ("swear", "swore", "sworn", "/sweə/", "so'kimoq", "клясться", "to swear"),
            ("sweep", "swept", "swept", "/swiːp/", "supurmoq", "подметать", "to sweep"),
            ("swim", "swam", "swum", "/swɪm/", "suzmoq", "плавать", "to swim"),
            ("teach", "taught", "taught", "/tiːtʃ/", "o'rgatmoq", "учить", "to teach"),
            ("throw", "threw", "thrown", "/θrəʊ/", "otmoq", "бросить", "to throw"),
            ("understand", "understood", "understood", "/ˌʌndəˈstʊd/", "tushunmoq", "понимать", "to understand"),
            ("wake", "woke", "woken", "/weɪk/", "uyg'otmoq", "будить", "to wake"),
            ("wear", "wore", "worn", "/weə/", "kiyish", "носить (одежду)", "to wear"),
            ("win", "won", "won", "/wʌn/", "yutmoq", "выиграть", "to win"),
            ("write", "wrote", "written", "/raɪt/", "yozmoq", "писать", "to write"),
            
            # Period 5 - Additional Common (20 verbs)
            ("forget", "forgot", "forgotten", "/fəˈɡɒt/", "unutmoq", "забыть", "to forget"),
            ("hide", "hid", "hidden", "/haɪd/", "yashirmoq", "прятать", "to hide"),
            ("mean", "meant", "meant", "/miːn/", "ma'no bildirmoq", "означать", "to mean"),
            ("read", "read", "read", "/riːd/", "o'qimoq", "читать", "to read"),
            ("cost", "cost", "cost", "/kɒst/", "narx bo'lmoq", "стоить", "to cost"),
            ("spread", "spread", "spread", "/spred/", "yoymoq", "распространять", "to spread"),
            ("hang", "hung", "hung", "/hæŋ/", "osmoq", "вешать", "to hang"),
            ("lend", "lent", "lent", "/lend/", "qarz berish", "одать в долг", "to lend"),
            ("bet", "bet", "bet", "/bet/", "garo qo'ymoq", "держать пари", "to bet"),
            ("broadcast", "broadcast", "broadcast", "/ˈbrɔːdkɑːst/", "efirga uzatmoq", "транслировать", "to broadcast"),
            ("creep", "crept", "crept", "/kriːp/", "suzib yurmoq", "ползти", "to creep"),
            ("dream", "dreamt", "dreamt", "/driːm/", "xayol qilmoq", "мечтать", "to dream"),
            ("lean", "leant", "leant", "/liːn/", "yotmoq", "наклоняться", "to lean"),
            ("leap", "leapt", "leapt", "/liːp/", "sakramoq", "прыгать", "to leap"),
            ("light", "lit", "lit", "/laɪt/", "yoqmoq", "зажечь", "to light"),
            ("smell", "smelt", "smelt", "/smel/", "hidlamoq", "нюхать", "to smell"),
            ("speed", "sped", "sped", "/spiːd/", "tez yurmoq", "мчаться", "to speed"),
            ("spell", "spelt", "spelt", "/spel/", "harflab yozmoq", "писать по буквам", "to spell"),
            ("spit", "spat", "spat", "/spɪt/", "tuflamoq", "плевать", "to spit"),
            ("split", "split", "split", "/splɪt/", "bo'lish", "раскалывать", "to split"),
        ]
        
        # Clear existing data
        Verb.objects.all().delete()
        
        # Create new entries
        for verb_data in verbs_data:
            Verb.objects.create(
                base_form=verb_data[0],
                past_simple=verb_data[1],
                past_participle=verb_data[2],
                pronunciation=verb_data[3],
                translation_uz=verb_data[4],
                translation_ru=verb_data[5] if len(verb_data) > 5 else verb_data[4],
                translation_en=verb_data[6] if len(verb_data) > 6 else verb_data[0],
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(verbs_data)} irregular verbs in 5 periods'))
