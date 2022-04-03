const header = document.getElementById('header-component');
header.innerHTML = `<head>
    <meta charset="UTF-8">
    <title>Jewelry Store</title>
    <style>
        nav a {
            color: #d64161;
            font-size: 1.5em;
            margin-left: 50px;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <nav>
        <a href="/products">Home</a>
        <a href="#">Account</a>
        <a href="/contact-us">Contact Us</a>
    </nav>
    <hr>
</body>`