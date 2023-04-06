const Action = {COMPLETE: "complete", REOPEN: "reopen", DELETE: "delete"};


const getToggleAction = action => action === Action.COMPLETE ? Action.REOPEN : Action.COMPLETE

const toggleTaskEntryComplete = (uid, btn) => {
    const action = getToggleAction(btn.getAttribute("data-action"));
    const task = document.getElementById(uid);
    task.classList.toggle("task-completed");
    btn.setAttribute("data-action", action);
    btn.classList.toggle("bi-check-lg");
    btn.classList.toggle("bi-repeat");
}


const removeTaskEntry = uid => {
    const taskContainer = document.getElementById("taskContainer");
    const task = document.getElementById(uid);
    taskContainer.removeChild(task);
}


const handleTaskAction = event => {
    const target = event.target.getAttribute("data-target");
    const action = event.target.getAttribute("data-action");

    if (action === Action.COMPLETE || action === Action.REOPEN) toggleTaskEntryComplete(target, event.target);
    if (action === Action.DELETE) removeTaskEntry(target);
}


const toggleTaskStatusButton = btn => {
    const action = getToggleAction(btn.getAttribute("data-action"));
    btn.classList.toggle("bi-check-lg");
    btn.classList.toggle("bi-repeat");
    btn.classList.toggle("btn-success");
    btn.classList.toggle("btn-primary");
    btn.setAttribute("data-action", action);
}


const toggleTaskStatus = event => {
    toggleTaskStatusButton(event.target);
}


const createCommentEntry = ({author, posted, message}) => {
    const containerClassList = ["comment-author", "comment", "d-flex", "mb-2"];

    const commentContainer = document.createElement("div");
    commentContainer.classList.add(...containerClassList);

    const avatar = document.createElement("img");
    commentContainer.appendChild(avatar);
    avatar.classList.add("rounded-circle", "shadow", "mx-3");
    avatar.src = author.img;

    const comment = document.createElement("div");
    commentContainer.appendChild(comment);
    comment.classList.add("card", "shadow", "px-5", "py-2");

    const commentAuthor = document.createElement("div");
    comment.appendChild(commentAuthor);
    commentAuthor.classList.add("author", "h5", "mb-2");
    commentAuthor.innerText = author.first_name + " " + author.last_name;

    const commentPosted = document.createElement("small");
    comment.appendChild(commentPosted);
    commentPosted.classList.add("small");
    commentPosted.innerText = posted;

    const commentMessage = document.createElement("p");
    comment.appendChild(commentMessage);
    commentMessage.innerText = message;

    return commentContainer;
}


const addComment = (comment) => {
    const container = document.getElementById("commentsContainer");
    container.insertBefore(comment, container.firstChild);
};


const handleSubmitComment = event => {
    event.preventDefault();
    event.stopPropagation();

    const message = document.querySelector("#commentForm input").value;
    event.target.reset();
    const payload = {
        "author": {
            "id": "598da43b",
            "img": "https://i.pravatar.cc/350?u=598da43b",
            "first_name": "Marmadoc",
            "last_name": "Brockhouse",
        },
        "posted": "Jan 27, 2023 04:45",
        message
    }
    addComment(createCommentEntry(payload));
}


const listActionButtons = document.querySelectorAll("#taskContainer .actions .btn.task-action");
listActionButtons.forEach(btn => btn.addEventListener("click", handleTaskAction));

const taskActionButton = document.querySelector("#taskActionsContainer .btn.task-action");
if (taskActionButton) taskActionButton.addEventListener("click", toggleTaskStatus);

const commentForm = document.getElementById("commentForm");
if (commentForm) commentForm.addEventListener("submit", handleSubmitComment);
