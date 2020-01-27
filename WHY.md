# Why TinyDevCRM?

I read through [this
article](https://spin.atomicobject.com/2020/01/24/new-software-project-questions/)
on 15 questions to ask at the start of a new software project, that I thought
would be a useful exercise to complete for TinyDevCRM.

## Product Discovery

### 1. What problem are we trying to solve? Why?

> Custom software is not cheap. Be sure to evaluate why your customer is looking
> to dive into it in the first place. Create space for all stakeholders to
> respond, as there are likely many different perspectives behind "the why".

I'm building TinyDevCRM primarily for my own use cases. The two problems I have
coming into this project include how to keep track of my habits for the long
term, and how to keep in touch with my personal professional network.

This expounded into a broader thought process as to how I can build a platform
that could generalize these two use cases, and future-proof against any other
use cases that would crop up with respect to my personal development workflows,
and perhaps some work-related use cases as well (e.g. a client process to remind
me to rotate my personal passwords, and rotate my work-related AWS IAM keys, in
order to follow AWS security best practices).

### 2. Is there a similar product on the market? If so, how will we differentiate from it?

> Benchmarking what other products exist is a great exercise to do during a
> Research, Design, and Planning phase. Use this time to understand how this
> product will be different. What value is it adding that others are lacking?

Here are some products that I've either used, tried out, or looked at when
thinking about whether I could get away with paying somebody else for a product
and work on something else.

**[Productive](http://productiveapp.io/) (USED)**: Productive is a generic iOS
habit tracker. I've used the product now for about two years or so, and so there
are things I absolutely love about the product and things I really don't like:

Pros:

-   **Natively mobile**: Productive ties extremely well with the iOS ecosystem,
    which means in-app push notifications (vs. having to install another native
    application like [Pushover](https://pushover.net/)), touch-first and
    swipe-first UI/UX, and portable wherever the iPhone goes.

-   **Offline-first access**: I don't need to have an Internet network
    connection through cellular or Wi-Fi in order to access or use the
    application.

-   **Forgiving UI/UX**: Unlike other habit trackers, Productive does not
    enforce default habits (you can start with however many habits makes you
    comfortable), default habit behaviors (a habit follows a specific grammar
    and is marked on that basis, does not couple with other instances of that
    habit), limit the number of habits available (some habit tracker apps do
    this as a premium feature), or set hard deadlines as to when habits can be
    marked as completed or skipped. This forgiving nature makes it very easy to
    forgive yourself when you lapse in your habit, and track your habits at your
    pace. This is likely the biggest reason I successfully onboarded and
    converted.

Cons:

-   **Application crashes and data loss**: Productive is highly secure, in the
    sense that data is colocated on the physical device, and only cloud-based
    iCloud and locally based iTunes backups are allowed.

    One problem with upgrading iOS applications is that downloading a fresh iOS
    application results in a different workflow than upgrading an existing iOS
    application. This means that cloud-based updates to the application, which
    their developers may mean to download from scratch, may not always work with
    older, existing deploys of the application. I'm sure they do their best, but
    on at least one occasion, an update bricked my application. Since I don't
    pay for iCloud, and since other cloud-based backup solutions are not
    available, and since I don't have a MacBook Pro available anymore for local
    iTunes backups (and I forgot the iTunes iPhone backup password), I couldn't
    restore the application to its prior state. This meant that all of my habits
    were simply lost and I had to start from scratch, which greatly disrupted my
    personal critical workflows.

    I would love to have a habit tracker that supports could-native backups,
    encrypted end-to-end and encrypted at-rest. [Standard
    Notes](https://standardnotes.org/), another application I use, has a (paid?)
    feature to email a copy of the entire encrypted copy of your data to your
    email, with a single-file HTML tool to decrypt that data given the latest
    encryption key registered on your cloud account, that you can then load into
    your native application. This is ideally the standard that the habit tracker
    I use would meet or exceed.

-   **Lack of third-party developer extensibility**: Productive.app is a closed
    environment with no available developer API. This means that additional
    analytics and view representations around habits cannot be tracked beyond
    what the app developers have provided. Currently, this is limited to what
    days of the month have you completed a specific habit.

-   **Opaque underlying data representation**: I have no idea how my data is
    saved. I would not be surprised if a NoSQL backing, and the lack of highly
    structured migrations, causes the application upgrade process to result in
    the data loss I've been experiencing.

Ultimately, I found the cons to outweigh the pros; the data loss and lack of
visibility into the underlying data representation and confidence in application
upgrades is especially egregious to my personal workflows. Considering how much
my personal workflow ties into how effective I am at other parts of my life, I
consider it my top pressure point. I do think the application stands heads and
shoulders above everything else I've tried (which is why I gladly pay money to
Productive for usage of the application), but I think I've acquired enough
skills to take a shot at this problem myself.

### 3. Are there other products or tools that we can, should, or need to integrate with?

> Does the product include a wearable device? Does it need to tie into other
> internal or external systems? Integrations will shape both the design and
> development approach, so knowing about them from the get-go is ideal.

## Business Discovery

### 4. What value are we providing to our business?

> Will the product help with sales? Will it provide impactful data? What is the
> reason our business is seeking to create the software?

### 5. What does success look like, and how will we measure it?

> Understanding expectations is crucial. Work with your team to create a shared
> understanding of what success is and how you might measure it.

### 6. What business risks or blockers exist?

> For example, is there a crucial integration that we need to work with IT on,
> but IT is booked out for 6 months? Is there a stakeholder who has the true
> vision of the product ,but they'll be on leave at the start of the project?

### 7. Who are the key stakeholders, and what kind of access will we have to them?

> Use this time to map out who your stakeholders are and set expectations for
> how engaged you will need them to be. How might you ensure the project never
> gets blocked from a lack of stakeholder feedback?

## User Discovery

### 8. Who will use the product?

> At the end of the day, we're building the software for people. Who are those
> people? What are their goals, motivations, and frustrations?

### 9. What value are we providing to users?

> Why would folks be inclined to use the tool we're creating? Understanding how
> we are providing value to users will help us determine which features to
> include and how to prioritize them.

### 10. What risks exist if a poor-intentioned user has access to the product?

> Though we'd love to assume only well-intentioned people will use our software,
> the reality is that this may not be true. What kind of trouble could occur if
> a villainous persona gets their hands on our software? Determine what the
> risks are so we can design to mitigate them?

### 11. Will we have access to users for research and testing?

> Having access to users is crucial for validating the overall product and
> workflows we create. Be sure to begin the process of locating and scheduling
> time with users as soon as you can.

## Project Discovery

### 12. What key dates exist?

> Is there an event where someone hopes to demo the software? Is the software
> itself tied to a specific time of year? It's important to know if there are
> date-sensitive deliverables to ensure on-time delivery is achieved.

### 13. What are the expected deliverables?

> The detailed scope of the projet will shape over time, but at the start of a
> project, high-level deliverables should be determined. Is it a mobile app? Is
> it an API? Does part of the project include training and onboarding the
> customer's developers once the product is ready to hand off?

### 14. Who is the primary decision maker?

> At the end of the day, who gets to make the final decisions? This ideally
> should be one person, in order to avoid a decision paralysis or design by
> committee.

### 15. How might we best work together?

> What are the communication preferences across the team? Will you be working
> on-site together, or remotely? How often and to what capacity can and will
> your stakeholders be involved? Set the cadence for the project. I recommend
> setting up recurring calendar events early on, well before calendars get full
> and you become blocked on stakeholder feedback.
