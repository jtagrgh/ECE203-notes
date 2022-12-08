// Write a clickable pwd string. Like a shell pwd
// but clickable and written in javascript.

current_path = window.location.pathname.split('/'); // Array of path directories
current_path.pop() // Remove last element "index.html"
web_root_pos = current_path.indexOf("ECE203-notes"); // Position in current_path array of root "203"
right_path = current_path.slice(web_root_pos); // Path [web_root, ]
left_path = current_path.slice(0, web_root_pos); // Path [system root, web_root)

for (p in right_path) {
    left_path.push(right_path[p]); // Add extend left_path w/ next dir
    path_str = left_path.join("/") + "/index.html"; // Actually link to index.html
    document.write("<a href=" + path_str + ">" + right_path[p] + "<a>/"); // Write to DOM
}
