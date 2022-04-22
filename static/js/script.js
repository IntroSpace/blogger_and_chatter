function changeLikedOfBlog(i) {
    cur_blog = document.getElementById("like-img-" + i);
    fetch('/api/blogs/change_like/' + i).then(function(response) {
      if (response.status == 200) {
        if (cur_blog.getAttribute('liked') == "True") {
            cur_blog.src = "https://cdn-icons-png.flaticon.com/512/2107/2107952.png";
            cur_blog.setAttribute("liked", "False");
        } else {
            cur_blog.src = "https://cdn-icons-png.flaticon.com/512/2107/2107774.png";
            cur_blog.setAttribute("liked", "True");
        }
      }
    });
};
function deleteBlogPost(i) {
    cur_blog = document.getElementById("blog-" + i);
    fetch('/api/blogs/admin/del/' + i).then(function(response) {
      if (response.status == 200) {
        document.getElementById('blog-1').remove()
      }
    });
};
function onclickListener(blog_id) {
    if (!document.elementFromPoint(event.clientX, event.clientY).classList.contains('other-click')) {
        window.location.pathname='/blog/' + blog_id;
    }
}