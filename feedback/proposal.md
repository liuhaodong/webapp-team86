Project proposal feedback
==================

**Team number**: 86<br>
**Team name**: WebChat<br>
**Team members**: haodongl, weiqingy

### Arthur
Writing a chat app is an extremely interesting challenge. However, there is a lot to do from a logistical standpoint (managing realtime updates, maintaining server and client state, etc). I'm worried that a lot of the project will be dealing with those issues rather than interesting server-side challenges using concepts we learned in the class. There is definitely a possibility of reframing the project so that it aligns a little more with the goals for the final project. Feel free to speak to Charlie or me to talk about more ideas!

### Bailey
You guys have an interesting idea, but in order for it to be a project of appropriate complexity, I would suggest that the complementary features be core features as well. In order to have a reasonably responsive chat client without excessive polling, I would recommend using websockets (https://developer.mozilla.org/en-US/docs/WebSockets). Here are some relevant django libraries: (https://www.djangopackages.com/grids/g/websockets/). If you don't use a realtime notification system like websockets, the user experience of the chat client will greatly suffer.

### Shannon
The project seems like it may be too small in scope. It seems closter to the appropriate scope if you include the complementary features as well as the rest of the core suggested features (and perhaps think about some other social features you can add). One large complication you may run into is that Django does not support real-time interaction (using web sockets or other techniques) very well. This means that you cannot push updates (i.e. new messages) to users unless they request them (which will not be in real-time). Because of this, you should think of using some other web framework like Node.js or Meteor. Being as this is the main component of your project, it is incredibly vital that you look into how you can integrate real-time interaction in a web application.

---

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/Team86/blob/master/feedback/proposal.md
