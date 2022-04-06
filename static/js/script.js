function changeLikedOfBlog(i) {
    cur_blog = document.getElementById("like-img-" + i);
    if (cur_blog.getAttribute('liked') == "True") {
        cur_blog.src = "https://cdn-icons-png.flaticon.com/512/2107/2107952.png";
        cur_blog.setAttribute("liked", "False");
    } else {
        cur_blog.src = "https://cdn-icons-png.flaticon.com/512/2107/2107774.png";
        cur_blog.setAttribute("liked", "True");
    }
    fetch('/api/blogs/change_like/' + i)
};
function onclickListener(blog_id) {
    if (!document.elementFromPoint(event.clientX, event.clientY).classList.contains('other-click')) {
        window.location.pathname='/blog/' + blog_id;
    }
}