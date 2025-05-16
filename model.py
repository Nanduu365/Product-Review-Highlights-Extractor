from dotenv import load_dotenv
import os
import subprocess
from google import genai
import json
# from text_extraction import VideoToTextExtractor, create_and_delete_folders,delete_files

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# create_and_delete_folders(['video_segments','audio_segments'])
# delete_files(['text_segments.txt'])

video_path = r'static\video\videoplayback.mp4'
video_segments_folder = 'video_segments'
audio_segments_folder = 'audio_segments'


# extractor = VideoToTextExtractor()
# extractor.scene_extractor(video_path=video_path, output_dir=video_segments_folder)
# # extractor.rename_extracted_scenes(video_segments_folder)
# extractor.audio_extractor(audio_dir=audio_segments_folder, video_dir=video_segments_folder)
# extractor.text_from_audio(audio_dir= audio_segments_folder)


system_prompt  = '''

ou are an AI assistant that classifies scenes in a video based on their speech transcript.

You must assign ONE of the following 4 titles to each scene:
1. none of the above
2. feature demonstration
3. product unboxing
4. final verdict

EXAMPLE:

scene 1:  First of all, I want to apologize.
scene 2:  I got a throat thing going on but look
scene 3:  I got a little bit of tea here, mint majesty.
scene 4:  We're gonna need that to stay clear.
scene 5:  We have an important video here today.  This is one of those packages that I receive.  It seems like yearly.
scene 6:  from China.
scene 7:  which acts as our best indication.
scene 8:  and our hands on experience.
scene 9:  with the next generation, I've shown before the next...
scene 10:  Next generation iPhone exists.
scene 11:  I believe what I have here is a 17 Pro Max.
scene 12:  I'm probably going to receive some more of these for different models, so make sure to subscribe,  so you don't miss that.  I mean, it's really your best look you're going to get at the next generation iPhone months  before it actually exists in hand.
scene 13:  people. So I'm gonna start with this box.
scene 14:  This is the real prime time, so don't leave the video, that's the real prime time, but we'll start with this.
scene 15:  as our first indication into...
scene 16:  to iPhone 17, but in.
scene 17:  The other package there is a much more...
scene 18:  or refined sample, then this one.  Now let's talk a little bit about room.
scene 19:  rumors as we jump in here, Apple is departing from it.
scene 20:  it's existing design.
scene 21:  definitely more so than it has in a while and a lot that has to do with how the
scene 22:  The camera section is going to be altered.
scene 23:  So this is an existing pro max iPhone 16 and a pro and obviously the non-pros this like triple
scene 24:  Everything has basically been the same for a long time.
scene 25:  this triangular shape also supporting the spatial video which is apparently a big deal to  Apple and one of the reasons.
scene 26:  Why they're going to maintain this triangular shape.
scene 27:  for the upcoming folks.
scene 28:  And they didn't opt for some of the other renders that people were putting out there with like a more stream line
scene 29:  or horizontal camera layout.
scene 30:  But the difference now...
scene 31:  is that you're having this two-tone thing going on.  So this is the first...
scene 32:  Seventeen Pro-Cable.
scene 33:  It actually has some really nice wheat.
scene 34:  it, but it's very crude, like it doesn't look like an actual phone. But the reason that these samples  exist is for case manufacturers to get a better idea of upcoming dimensions so they're ready  to sell in the phone actually.
scene 35:  Now a lot of these you've seen online, you've seen photos of these online, you probably haven't seen them in the hand.
scene 36:  I'm like I said in this other package here.
scene 37:  We're going to take things up a notch with a lot more detail.
scene 38:  and a much more refined.
scene 39:  kind of sample. 17 probably can see it.
scene 40:  This one actually has dimensions listed on it as well, which I think is interesting.  149.63, 71.44, and 8.75.
scene 41:  Now the other thing, which appears to be true in this case using this example, is that it's getting a little bit fatter.  And that's it.
scene 42:  Actually, that looks true, just whole-
scene 43:  at there compared to the previous generation pro, it definitely looks fodder.
scene 44:  Now does that mean...
scene 45:  bigger battery? Yes, most likely. Not by a huge margin, but slightly bigger.
scene 46:  If the other rumors...
scene 47:  that are likely to be true here.
scene 48:  Faster wireless charging reverse wireless charging so more components in there faster wired charging hopefully jump it up to 35
scene 49:  That's nothing compared to those flagship Android phones.
scene 50:  better. No one's getting complain about faster charging. Obviously we've still got our camera control button.
scene 51:  The other thing, a lot of these models seem to...
scene 52:  to highlight this MagSafe portion and also create this outline for this rectangular section  of the back.
scene 53:  and that's because
scene 54:  Unlike on previous generations with all
scene 55:  The whole thing is essentially this matte glass and then you've only got this titanium frame.
scene 56:  Suppose the frame here is actually going to be
scene 57:  Illuminum now, not titanium, it'll make it a little bit more lightweight.
scene 58:  Anyway, and then you'll just have this small portion of glass in...
scene 59:  The center, at least that's the prevailing rumor, otherwise button lay out similar.
scene 60:  You can see they move the flash all the way.
scene 61:  over to the other side. There were some rumors that they were going to...
scene 62:  Damn, a little screen in here.
scene 63:  For better selfie video or something. I don't think that's gonna happen. That's pipe dream stuff
scene 64:  However, the other portion to mention, with your dynamic island which still exists there,
scene 65:  the front facing cameras said to see an improvement.
scene 66:  up to 24 megapixels. Obviously a new chip, faster device, slightly bigger battery.
scene 67:  but I don't know how people feel about the design, which is like the main kind of change  and the fact that you go to a two-tone setup with...
scene 68:  A lot less glass.
scene 69:  Okay, let's pull out the caliper real quick. What is it?
scene 70:  say on the caliper here it says.
scene 71:  It's time for five, so what do you say?  Yeah.
scene 72:  we are talking about millimeters so
scene 73:  They're saying that the iPhone 17 Pro 8.75...
scene 74:  5 mm thick, 71.44 mm wide, and 149.63 mm tall.
scene 75:  and so that makes it bigger.
scene 76:  and the previous generation of probably just makes it slightly bigger.
scene 77:  and pretty much every way.
scene 78:  Now maybe the reason for that is because of this rumored iPhone 17.
scene 79:  As I suggest at the beginning of the video, as I receive more of these models...
scene 80:  I'm going to show off those compare them to these.
scene 81:  And that's likely coming up in a future video, so make sure to subscribe.
scene 82:  So you don't miss that all right now. Let's go ahead and jump inside the magic package
scene 83:  But before we do, actually, let's talk a little bit about this.
scene 84:  funny little mic that I'm wearing.
scene 85:  on my hat. Thank you too.
scene 86:  Holy Land for sponsoring this episode.  This is my go-to mic.
scene 87:  a wearable mic and normally I would have wear it on my hat but I'm actually trying to call it out.
scene 88:  This is like the tiniest little, most convenient clip for you, if you hope to make content.
scene 89:  online. It has this little charge kit.
scene 90:  that it can interface directly with your smartphone if...
scene 91:  That's how you record. You can do interviews with a two-pack.
scene 92:  That's included everything stays charged in this little guy.
scene 93:  and it's got a tiny little r-
scene 94:  seever as well, which can plug into your camera if you
scene 95:  use a dedicated camera and you don't want to record directly into the smartphone and it  all is in this little kit which charges up over USB-C and then you've also got a travel  bag to keep everything secure. So I've been using their product for a while and I want to use it in
scene 96:  This video just to show you how close you...
scene 97:  you can get it to an actual studio microphone even though.
scene 98:  It's tiny and wearable and you can really just clip this mic anywhere and of course it's wireless
scene 99:  Check out the range, like I can just...
scene 100:  keep moving, but I still sound like...
scene 101:  I'm sitting right there.
scene 102:  And here's a little easter egg, there's actually some video of Apple's CEO Tim Cuff wearing this exact M2S, the last time he visited China.
scene 103:  So if you're looking for the perfect little microphone kit to pair with your eventual iPhone 17
scene 104:  Look at this, check this out. Boom, it's a little guy plugs in the bottom. Now you've got a whole production for sale
scene 105:  with the phone that's already in your pocket.
scene 106:  and an entire microphone kit that also fits in your box, perfect.
scene 107:  Let's...
scene 108:  Move on here to the main attraction of this video.
scene 109:  And the reason you clicked on this video inside this package right here.
scene 110:  I believe it's one of one.
scene 111:  at the moment, a high quality production.
scene 112:  and hands-on with the closest sample yet.
scene 113:  to the iPhone 17 Pro Max.
scene 114:  It's amazing.
scene 115:  level of detail that they can go into on some of these things.
scene 116:  This one gets its own lock bag, velvety bag.
scene 117:  So, there it is, the iPhone 17 Pro Max.
scene 118:  It's kind of weird looking, honestly.
scene 119:  That's a little bit hard for me to believe.  Some seem to suggest maybe it's inspired by the watch.  Like, are you feeling that kind of just compare?
scene 120:  from like which is more beautiful to you.  That's going to take a little while to get used with the two-tone thing.
scene 121:  It's definitely a departure.
scene 122:  People are going to know that you're using the 17 Pro Max and not the 16, 15 or otherwise.
scene 123:  At least initially, I'm not sure that it's as good-looking.
scene 124:  Everybody always gets used to these designs, but initially it's just this big gap and then having the flash all the way over there looking around
scene 125:  On the device otherwise, very simple.
scene 126:  Well, while this even has a functioning, look at...
scene 127:  that that's actually the pins in there for the type C. This feels like a fit.
scene 128:  product honestly. This is one of the nicest singular manufactured one-offs that I've ever
scene 129:  to receive. Look at this thing. Anyway, everything as far as the layout remains the same,  exactly the same. Even the sim tray is in the same location, power control, power, the...
scene 130:  camera modules
scene 131:  themselves. Ah, they look roughly the same size. Display size...
scene 132:  looks pretty much identical. It's a huge phone still. You can see.
scene 133:  It's visibly thicker this new design at least
scene 134:  in the non-camera sections. If we want to do...
scene 135:  you a quick wobble test.
scene 136:
scene 137:
scene 138:  Okay.
scene 139:  slightly less wobb.
scene 140:  Well, there it is, got-
scene 141:  the iPhone 17 Pro Max. Are you guys happy with this? What do you think? Like is it going to grow on you? Is that?
scene 142:  something you see as an improvement to the previous generation we're talking
scene 143:  just about the design obviously there.
scene 144:  are going to be hardware improvements the device is going to have the new chip it will be faster the cameras are all said to be improved 48 megapixels all the way around
scene 145:  They maintain their horrors until set up.
scene 146:  for the purpose of spatial video.
scene 147:  from facing camera also gets an improvement. Reverse wireless charging is the room or faster charging.
scene 148:  design work.
scene 149:  iPhone 16 Pro Max or 17 Pro Max, what do you think?
scene 150:  I don't know what people are going to think. I honestly like some people could call it ugly.  I really do, but it's an iPhone.  You know there's going to be about a billion of these things hidden in the market all at once,  and then people are just going to get used to it, and then a bunch of other companies will copy it.  That's just the future of our lives, whether we like it or not.  Now, the trend has been set. We're going to see funny, two-tone type of smartphones hidden in the market.  And it's a market that desperately needs something to feel new, anyhow.  Been a long, it's been a long time like this.
scene 151:  And then they're like
scene 152:  So, well...
scene 153:  It's like...
scene 154:  The Bigger
scene 155:  better.
scene 156:  specs.
scene 157:  other improvements. Now we're titanium and then they're like now we're not at least a
scene 158:  Again, that's the room. I mean, this looks like a loop.
scene 159:  Anyway, there you have it iPhone 17 Pro Max the best look yet that you're gonna get what it's gonna be like to have it to hold it to
scene 160:  diet if you choose to
scene 161:  Pricing, supposedly going to start around 1250 USD.
scene 162:  They're gonna be pricey beasts and they're gonna be out relatively shortly and as I mentioned at the beginning of this
scene 163:  video. I may have some other very nice models coming in shortly so make sure to subscribe if you want to see those  comparatively and also if you're in the market
scene 164:  for any kind of microphone.
scene 165:  Improvement in your audio production.
scene 166:  Whether you're shooting on a smartphone or a camera, you've got to check out our partners at Hollywood.
scene 167:  and they're making some really cool stuff  and this little device is my favorite.  Oh yeah, another thing.
scene 168:  Maybe you don't love it.
scene 169:  The two-tone design.
scene 170:  and you're gonna put a case on it.
scene 171:  You could always go with a later case.  Look at that.  One toe, super thin, so you're newer, fatter-eyed.
scene 172:  phone doesn't have to feel
scene 173:  any fatter than that. So yeah, if you haven't yet check out later case super crazy thin phone cases for your existing iPhone or your new
scene 174:  iPhone 17 Pro Max.



JSON Response:
{
  "scene 1": {
    "title": "none of the above"
  },
  "scene 2": {
    "title": "none of the above"
  },
  "scene 3": {
    "title": "none of the above"
  },
  "scene 4": {
    "title": "none of the above"
  },
  "scene 5": {
    "title": "none of the above"
  },
  "scene 6": {
    "title": "none of the above"
  },
  "scene 7": {
    "title": "none of the above"
  },
  "scene 8": {
    "title": "none of the above"
  },
  "scene 9": {
    "title": "none of the above"
  },
  "scene 10": {
    "title": "none of the above"
  },
  "scene 11": {
    "title": "product unboxing"
  },
  "scene 12": {
    "title": "none of the above"
  },
  "scene 13": {
    "title": "product unboxing "
  },
  "scene 14": {
    "title": "none of the above"
  },
  "scene 15": {
    "title": "product unboxing"
  },
  "scene 16": {
    "title": "product unboxing"
  },
  "scene 17": {
    "title": "product unboxing"
  },
  "scene 18": {
    "title": "product unboxing"
  },
  "scene 19": {
    "title": "product unboxing"
  },
  "scene 20": {
    "title": "product unboxing"
  },
  "scene 21": {
    "title": "product unboxing"
  },
  "scene 22": {
    "title": "product unboxing"
  },
  "scene 23": {
    "title": "none of the above"
  },
  "scene 24": {
    "title": "none of the above"
  },
  "scene 25": {
    "title": "none of the above"
  },
  "scene 26": {
    "title": "none of the above"
  },
  "scene 27": {
    "title": "none of the above"
  },
  "scene 28": {
    "title": "none of the above"
  },
  "scene 29": {
    "title": "none of the above"
  },
  "scene 30": {
    "title": "product unboxing"
  },
  "scene 31": {
    "title": "product unboxing"
  },
  "scene 32": {
    "title": "product unboxing"
  },
  "scene 33": {
    "title": "feature demonstration"
  },
  "scene 34": {
    "title": "feature demonstration"
  },
  "scene 35": {
    "title": "none of the above"
  },
  "scene 36": {
    "title": "none of the above"
  },
  "scene 37": {
    "title": "none of the above"
  },
  "scene 38": {
    "title": "none of the above"
  },
  "scene 39": {
    "title": "feature demonstration"
  },
  "scene 40": {
    "title": "feature demonstration"
  },
  "scene 41": {
    "title": "feature demonstration"
  },
  "scene 42": {
    "title": "feature demonstration"
  },
  "scene 43": {
    "title": "feature demonstration"
  },
  "scene 44": {
    "title": "feature demonstration"
  },
  "scene 45": {
    "title": "feature demonstration"
  },
  "scene 46": {
    "title": "feature demonstration"
  },
  "scene 47": {
    "title": "feature demonstration"
  },
  "scene 48": {
    "title": "feature demonstration"
  },
  "scene 49": {
    "title": "feature demonstration"
  },
  "scene 50": {
    "title": "feature demonstration"
  },
  "scene 51": {
    "title": "feature demonstration"
  },
  "scene 52": {
    "title": "feature demonstration"
  },
  "scene 53": {
    "title": "feature demonstration"
  },
  "scene 54": {
    "title": "feature demonstration"
  },
  "scene 55": {
    "title": "feature demonstration"
  },
  "scene 56": {
    "title": "feature demonstration"
  },
  "scene 57": {
    "title": "feature demonstration"
  },
  "scene 58": {
    "title": "feature demonstration"
  },
  "scene 59": {
    "title": "feature demonstration"
  },
  "scene 60": {
    "title": "feature demonstration"
  },
  "scene 61": {
    "title": "feature demonstration"
  },
  "scene 62": {
    "title": "feature demonstration"
  },
  "scene 63": {
    "title": "feature demonstration"
  },
  "scene 64": {
    "title": "feature demonstration"
  },
  "scene 65": {
    "title": "feature demonstration"
  },
  "scene 66": {
    "title": "feature demonstration"
  },
  "scene 67": {
    "title": "feature demonstration"
  },
  "scene 68": {
    "title": "feature demonstration"
  },
  "scene 69": {
    "title": "feature demonstration"
  },
  "scene 70": {
    "title": "feature demonstration"
  },
  "scene 71": {
    "title": "feature demonstration"
  },
  "scene 72": {
    "title": "feature demonstration"
  },
  "scene 73": {
    "title": "feature demonstration"
  },
  "scene 74": {
    "title": "feature demonstration"
  },
  "scene 75": {
    "title": "feature demonstration"
  },
  "scene 76": {
    "title": "feature demonstration"
  },
  "scene 77": {
    "title": "feature demonstration"
  },
  "scene 78": {
    "title": "feature demonstration"
  },
  "scene 79": {
    "title": "none of the above"
  },
  "scene 80": {
    "title": "none of the above"
  },
  "scene 81": {
    "title": "none of the above"
  },
  "scene 82": {
    "title": "none of the above"
  },
  "scene 83": {
    "title": "none of the above"
  },
  "scene 84": {
    "title": "none of the above"
  },
  "scene 85": {
    "title": "none of the above"
  },
  "scene 86": {
    "title": "none of the above"
  },
  "scene 87": {
    "title": "none of the above"
  },
  "scene 88": {
    "title": "none of the above"
  },
  "scene 89": {
    "title": "none of the above"
  },
  "scene 90": {
    "title": "none of the above"
  },
  "scene 91": {
    "title": "none of the above"
  },
  "scene 92": {
    "title": "none of the above"
  },
  "scene 93": {
    "title": "none of the above"
  },
  "scene 94": {
    "title": "none of the above"
  },
  "scene 95": {
    "title": "none of the above"
  },
  "scene 96": {
    "title": "none of the above"
  },
  "scene 97": {
    "title": "none of the above"
  },
  "scene 98": {
    "title": "none of the above"
  },
  "scene 99": {
    "title": "none of the above"
  },
  "scene 100": {
    "title": "none of the above"
  },
  "scene 101": {
    "title": "none of the above"
  },
  "scene 102": {
    "title": "none of the above"
  },
  "scene 103": {
    "title": "none of the above"
  },
  "scene 104": {
    "title": "none of the above"
  },
  "scene 105": {
    "title": "none of the above"
  },
  "scene 106": {
    "title": "none of the above"
  },
  "scene 107": {
     "title": "none of the above"
  },
  "scene 108": {
    "title": "none of the above"
  },
  "scene 109": {
    "title": "none of the above"
  },
  "scene 110": {
    "title": "product unboxing"
  },
  "scene 111": {
    "title": "product unboxing"
  },
  "scene 112": {
    "title": "product unboxing"
  },
  "scene 113": {
    "title": "product unboxing"
  },
  "scene 114": {
    "title": "product unboxing"
  },
  "scene 115": {
    "title": "product unboxing"
  },
  "scene 116": {
    "title": "product unboxing"
  },
  "scene 117": {
    "title": "product unboxing"
  },
  "scene 118": {
    "title": "feature demonstration"
  },
  "scene 119": {
    "title": "feature demonstration"
  },
  "scene 120": {
    "title": "feature demonstration"
  },
  "scene 121": {
    "title": "feature demonstration"
  },
  "scene 122": {
    "title": "feature demonstration"
  },
  "scene 123": {
    "title": "feature demonstration"
  },
  "scene 124": {
    "title": "feature demonstration"
  },
  "scene 125": {
    "title": "feature demonstration"
  },
  "scene 126": {
    "title": "feature demonstration"
  },
  "scene 127": {
    "title": "feature demonstration"
  },
  "scene 128": {
    "title": "feature demonstration"
  },
  "scene 129": {
    "title": "feature demonstration"
  },
  "scene 130": {
    "title": "feature demonstration"
  },
  "scene 131": {
    "title": "feature demonstration"
  },
  "scene 132": {
    "title": "feature demonstration"
  },
  "scene 133": {
    "title": "feature demonstration"
  },
  "scene 134": {
    "title": "feature demonstration"
  },
  "scene 135": {
    "title": "feature demonstration"
  },
  "scene 136": {
  },
  "scene 137": {
    "title": "none of the above"
  },
  "scene 138": {
    "title": "none of the above"
  },
  "scene 139": {
    "title": "feature demonstration"
  },
  "scene 140": {
    "title": "feature demonstration"
  },
  "scene 141": {
    "title": "feature demonstration"
  },
  "scene 142": {
    "title": "feature demonstration"
  },
  "scene 143": {
    "title": "feature demonstration"
  },
  "scene 144": {
    "title": "feature demonstration"
  },
  "scene 145": {
    "title": "feature demonstration"
  },
  "scene 146": {
    "title": "feature demonstration"
  },
  "scene 147": {
    "title": "feature demonstration"
  },
  "scene 148": {
    "title": "feature demonstration"
  },
  "scene 149": {
    "title": "feature demonstration"
  },
  "scene 150": {
    "title": "feature demonstration"
  },
  "scene 151": {
    "title": "feature demonstration"
  },
  "scene 152": {
    "title": "feature demonstration"
  },
  "scene 153": {
    "title": "feature demonstration"
  },
  "scene 154": {
    "title": "feature demonstration"
  },
  "scene 155": {
       "title": "feature demonstration"
  },
  "scene 156": {
      "title": "feature demonstration"
  },
  "scene 157": {
    "title": "feature demonstration"
  },
  "scene 158": {
    "title": "feature demonstration"
  },
  "scene 159": {
    "title": "final verdict"
  },
  "scene 160": {
    "title": "final verdict"
  },
  "scene 161": {
    "title": "final verdict"
  },
  "scene 162": {
    "title": "none of the above"
  },
  "scene 163": {
    "title": "none of the above"
  },
  "scene 164": {
    "title": "none of the above"
  },
  "scene 165": {
    "title": "none of the above"
  },
  "scene 166": {
    "title": "none of the above"
  },
  "scene 167": {
    "title": "none of the above"
  },
  "scene 168": {
    "title": "none of the above"
  },
  "scene 169": {
    "title": "none of the above"
  },
  "scene 170": {
    "title": "none of the above"
  },
  "scene 171": {
    "title": "none of the above"
  },
  "scene 172": {
    "title": "none of the above"
  },
  "scene 173": {
    "title": "none of the above"
  },
  "scene 174": {
    "title": " "
  }
}


EXAMPLE:

scene 0:  
scene 1:  
scene 2:   Alright, I think we can make this pretty short and sweet.  The Mac team is on one.
scene 3:   To the M4 Mac Mini Refreshed was already one of the best tech deals of all 2024, great computer, great price.  So now here.
scene 4:   Here comes this new M4 MacBook Air.  It's the most capable, powerful version yet, obviously.
scene 5:   to the new chip. The starting memory is 16 gigs. It gets a sneaky slightly larger battery,  some Thunderbolt improvements, a new webcam.
scene 6:   And new color and the price goes down.
scene 7:   It's kind of funny looking back a bit at the arc of reviewing MacBook Airs over the year.
scene 8:   Like at first it was this spectacle of engineering, but also kind of in practical and missing a few ports.
scene 9:   They went from that to being a bit of an outdated design, but improving a lot.
scene 10:  Then turned into basically the easiest to recommend laptop in the world at 999 with
scene 11:  Then, with Apple Silicon updates and higher base storage, the price did go up with the M2 generation by 200 bucks, so it was 11.99, and I feel like everyone just kind of went.  Alright, it's still fine. Yeah, it's still a good laptop for that price.
scene 12:  But now it's 2025 and it's got the M4 chip  and the price has dropped back down to 999  for the base machine again, and that is...
scene 13:   Now, almost nothing else has physically changed with the slap top.  Still the same keyboard, you know, there's no speaker grills.
scene 14:   They're still max-safe charging, 2 USB-Type C ports.
scene 15:   The headphone jack, the notch at the top of the...
scene 16:   60 Hertz LCD, the thin and light aluminum build.  This is very,
scene 17:   are still the MacBook Air. If you want to get sweaty about it, as they've 2D was
scene 18:   the mute button icon is different and the webcam.
scene 19:   is now a 12 megapixel center stage webcam, which can follow you around the frame if you leave  it on, but I actually do turn it off every time.  And also,
scene 20:   So I noticed on Apple's website, the battery capacity went up slightly from 52.6 watt hours to 53.8 watt hours, this generation, so that's about 2% more capacity.
scene 21:   Pay attention, okay. It's a real-life spot the difference is challenge, but really the main way obviously will know if it's the new laptop generation or not is this
scene 22:   Did you notice it's a, it's a new color, uh, barely.
scene 23:   It's called sky blue this time.  If I could rename it, I'd rename it.
scene 24:   Barely blue considering when it's up against white backgrounds. Okay, it looks a little bit blue, but when it's up against actually blue things  It literally looks silver again. It's
scene 25:   like the La Croix of Macbook Paint Colors.
scene 26:   It's like someone whispered the word blue in the paint shop just before placing each one  in its box and shipping it away. But yeah, now you know if you see this pale blue color  on a MacBook Air, it notes the new one. This replaces Space Gray.
scene 27:   But also speaking of boxes, this is the box that my MacBook Air came in from Apple, the review unit, and I don't know if you'd notice on the corner there.
scene 28:   It appears someone has bled onto the box of this computer.  I don't really know how that happens.  I just pulled it out of the cardboard shipping box,  and it just looked like this.  Really weird, never seen that before.
scene 29:   I really hope whoever package this computer is okay.  Anyway.
scene 30:   But the main reason this laptop is such a big deal is the chip, right?  This M4 chip, it's...
scene 31:   Really good. We already learned this from the M4 iPad Pro 9 months ago and then again with the M4 Mac Mini 4 months ago
scene 32:   This chip in the laptop will be passively cooled, so no fans in the air on like the Mac Mini.  So, yeah, sustained performance ceiling is going to be a bit lower.
scene 33:   But for the quick, bursty stuff, like normal computer activities, yeah, it's amazing, as expected.  And in the specific benefit in case you forgot of the M4 over previous generations of Apple Silicon,
scene 34:   It's going to be more AI-specific horsepower, so more powerful 16-core neural engine.
scene 35:   And some of that manifests itself in useless stuff like image playground, rendering images  locally faster than ever before, cool.
scene 36:   But also some of that is potentially useful stuff like the background cutouts being quicker and more accurate or the same
scene 37:   We'll click photo enhancer in Pixelmator Pro being much faster.
scene 38:   reviewing MacBook Airs is so funny though because we do this every time.  This is the baseline.  This is the cheapest entry-level way to get a Mac laptop for people who don't care about  pro-level tasks. They're just going to check their email and  web browser and maybe edit a photo once in a while.  Basic stuff, MacBook Air, classic.  But because Apple Silicon has gotten so good, we end up  able to do things that are a way beyond that. This machine is capable of things that require  to pro-ship like a couple of years ago. That's not an exaggeration.
scene 39:   So when I tell you I could load up a bunch of 4K and 8K footage into a final clip.
scene 40:   That prototype line, and it would scrub through the timeline with almost no hesitation  at quarter-risk playback resolution, and then it could export the project  just a few beats slower than a Mac mini.
scene 41:   That literally doesn't matter to 99% of MacBook Air buyers.
scene 42:   But the chip is so powerful, it's capable of it, so it's just good to know that you could.
scene 43:   You know, most airs will never have 3D modeling applications, or logic pro, or ever be  churning through the Adobe suite or plan.
scene 44:   on AAA games, but instead they'll be doing video calls and having 20 safari tabs open  and we're flipping through a bunch of productivity apps.
scene 45:   But it is pretty sick that this computer can stretch  and handle all of that.  So do you choose to throw that at it?  That is the modern MacBook Air.  There's even a allegedly a customer  that was frustrated with the last generation of air,  because it couldn't connect two different six K displays  at the same time and use them with the lid open.  And so now, this one can.
scene 46:   It's okay, great. This laptop is still a great machine and a great deal.  Here's my only complaint, potentially, with this laptop.  I would like a better display.  Now, I know that I'm coming from a MacBook Pro, and I'm very used to these really good displays,  and it seems like Apple is as they usually do,  observing certain things for the pros, so the mini LED.
scene 47:   the pro-res high refresh rate even the nanotextre coating on the display.
scene 48:   All that stuff is reserved for the MacBook Pro, but all that is stuff that I would like to see in a MacBook Air.  And I think I could handle it. I think it's got plenty of battery. It's got it could go brighter. It could look even better.  So I want a better screen on the MacBook Air, me personally as an option, but I, again, I know that most people won't even notice and will be totally fine with this.
scene 49:   Here's a more important question that I ask basically every year with this MacBook Pro,  because we always talk about this base price.  Can you actually order the base price spec and still be fine?  And this year, again, I feel like for most people, the answer actually is yes.
scene 50:   because this time that's 16 gigs of unified memory and then it's 256 gigs of base storage.  So the storage and memory upgrades are always borderline robbery. That's not a shocker.  Like, I do like that you can get a much faster charger for 20 bucks if you don't already have one.  But yeah.
scene 51:   Doubling up to 16 gigs based for 999 is huge since these computers can go to SWAT memory so quickly.
scene 52:   Shout out to the single best feature of Apple Intelligence, which has been improving the  matter of RAM in every Apple device.
scene 53:   If you are in the market for a base machine, though, I think if you don't plan on ever doing  super high-end tasks, you can still consider the last gen that is going to sound familiar,  but the last gen is also a really good deal.  It has half that memory eight gigs, but it's...
scene 54:   The 99 had best by right now.
scene 55:   So that's a really good deal. Obviously, if you have an older MacBook, if you have an Intel MacBook,  this is the type of stuff you're going to be looking at. Otherwise then, yeah, pretty easy  to recommend the baseline, the new entry level sky blue MacBook Air.
scene 56:   All things considered it's pretty boring that this laptop doesn't change very much,  and it's just a barely new color, and it's a chip we've already seen before.  But I think it's pretty exciting that laptops have gotten this good period.  Thanks for watching.  Catch you guys in the next one. Peace.
scene 57:   Thanks for watching, and I'll see you in the next video!



JSON Response:
{
  "scene 0": {
    "title": "none of the above"
  },
  "scene 1": {
    "title": "none of the above"
  },
  "scene 2": {
    "title": "none of the above"
  },
  "scene 3": {
    "title": "none of the above"
  },
  "scene 4": {
    "title": "product_unboxing"
  },
  "scene 5": {
    "title": "feature demonstration"
  },
  "scene 6": {
    "title": "feature demonstration"
  },
  "scene 7": {
    "title": "none of the above"
  },
  "scene 8": {
    "title": "none of the above"
  },
  "scene 9": {
    "title": "none of the above"
  },
  "scene 10": {
    "title": "none of the above"
  },
  "scene 11": {
    "title": "none of the above"
  },
  "scene 12": {
    "title": "feature demonstration"
  },
  "scene 13": {
    "title": "feature demonstration"
  },
  "scene 14": {
    "title": "feature demonstration"
  },
  "scene 15": {
    "title": "feature demonstration"
  },
  "scene 16": {
    "title": "feature demonstration"
  },
  "scene 17": {
    "title": "feature demonstration"
  },
  "scene 18": {
    "title": "feature demonstration"
  },
  "scene 19": {
    "title": "feature demonstration"
  },
  "scene 20": {
    "title": "feature demonstration"
  },
  "scene 21": {
    "title": "none of the above"
  },
  "scene 22": {
    "title": "feature demonstration"
  },
  "scene 23": {
    "title": "none of the above"
  },
  "scene 24": {
    "title": "feature demonstration"
  },
  "scene 25": {
    "title": "none of the above"
  },
  "scene 26": {
    "title": "none of the above"
  },
  "scene 27": {
    "title": "none of the above"
  },
  "scene 28": {
    "title": "none of the above"
  },
  "scene 29": {
    "title": "none of the above"
  },
  "scene 30": {
    "title": "feature demonstration"
  },
  "scene 31": {
    "title": "feature demonstration"
  },
  "scene 32": {
    "title": "feature demonstration"
  },
  "scene 33": {
    "title": "feature demonstration"
  },
  "scene 34": {
    "title": "feature demonstration"
  },
  "scene 35": {
    "title": "feature demonstration"
  },
  "scene 36": {
    "title": "feature demonstration"
  },
  "scene 37": {
    "title": "feature demonstration"
  },
  "scene 38": {
    "title": "final verdict"
  },
  "scene 39": {
    "title": "final verdict"
  },
  "scene 40": {
    "title": "final verdict"
  },
  "scene 41": {
    "title": "final verdict"
  },
  "scene 42": {
    "title": "none of the above"
  },
  "scene 43": {
    "title": "feature demonstration"
  },
  "scene 44": {
    "title": "feature demonstration"
  },
  "scene 45": {
    "title": "none of the above"
  },
  "scene 46": {
    "title": "final verdict"
  },
  "scene 47": {
    "title": "final verdict"
  },
  "scene 48": {
    "title": "final verdict"
  },
  "scene 49": {
    "title": "final verdict"
  },
  "scene 50": {
    "title": "final verdict"
  },
  "scene 51": {
    "title": "none of the above"
  },
  "scene 52": {
    "title": "final verdict"
  },
  "scene 53": {
    "title": "final verdict"
  },
  "scene 54": {
    "title": "final verdict"
  },
  "scene 55": {
    "title": "final verdict"
  },
  "scene 56": {
    "title": "final verdict"
  },
  "scene 57": {
    "title": "none of the above"
  }
}


USER:

'''

def preprocess_prompt(system_prompt, text_segments_file, event):
    '''Take the text from txt file and format it in a properform for 
    making the prompt for model'''
    if not event.is_set():
      with open(text_segments_file, 'r') as f:
          lines = f.readlines()

      # user_prompt = [ f'scene {i}:' + line  for i,line in enumerate(lines)]
      user_prompt = "".join(lines) # \n is already there, so no space is added for the join
      # print(lines)
      print(f'Total No of scenes : {len(lines)}')

    return system_prompt+user_prompt
    

def generate_response(query, event,api_key = GOOGLE_API_KEY):

  if not event.is_set():
    # print(query)
    client = genai.Client(api_key = api_key)

    response = client.models.generate_content(
        model = "gemini-2.5-flash-preview-04-17",
        contents = [query],
        config={
          "response_mime_type": "application/json",
          "temperature": 0.2}
    )

    json_response =json.loads(response.text)

  return json_response
  


#Scene by scene video collection from text

def merge_videos(video_segments_folder,json_response, event):

  none_of_the_above = []
  feature_demonstration = []
  product_unboxing = []
  final_verdict = []


  for i in range(len(os.listdir(video_segments_folder))):

    if not event.is_set():
      title = json_response[f'scene {i}']['title']
      print(f'\r{i}', end = '')

      path_to_video = os.path.join(video_segments_folder,f'-Scene-{i}.mp4')
      # path_to_video = path_to_video.replace(r'\-', '/-')

      if title == 'none of the above':
        none_of_the_above.append(path_to_video)
      elif title == 'feature demonstration':
        feature_demonstration.append(path_to_video)
      elif title == 'product unboxing':
        product_unboxing.append(path_to_video)
      elif title == 'final verdict':
        final_verdict.append(path_to_video)


  with open(r'join_videos\none_of_the_above.txt','w') as f:
    for path in none_of_the_above:
      f.write(f"file '{path}'\n")

  with open(r'join_videos\product_unboxing.txt','w') as f: 
    for path in product_unboxing:
      f.write(f"file '{path}'\n")

  with open(r'join_videos\feature_demonstration.txt','w') as f:
    for path in feature_demonstration:
      f.write(f"file '{path}'\n")

  with open(r'join_videos\final_verdict.txt','w') as f:
    for path in final_verdict:
      f.write(f"file '{path}'\n")

  for txt in ['none_of_the_above','product_unboxing','feature_demonstration','final_verdict']:
    # subprocess.run(['ffmpeg','-f','concat','-safe','0',
    #               '-i',f'{txt}.txt',
    #                 '-c:v','libx264','-c:a','aac','-strict','-2',
    #               f'results/{txt}.mp4'])
    if not event.is_set():
      subprocess.run([
      'ffmpeg',
      '-safe', '0',
      '-f', 'concat',
      '-i', rf'join_videos\{txt}.txt',
      '-vsync', 'vfr',
      '-c:v', 'libx264',
      '-preset', 'fast',
      '-crf', '23',
      '-c:a', 'libvo_aacenc',
      '-b:a', '192k',
      f'results/{txt}.mp4'
      ])


    

# query = preprocess_prompt(system_prompt,'text_segments.txt')
# # print(query)
# json_response = generate_response(query)
# print(json_response)


# merge_videos(video_segments_folder,json_response)

# print(json_response)