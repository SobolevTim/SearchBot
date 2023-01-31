<body>
<h1>SearchBot from Telegram</h1>
<p>This is a bot created for the factory. Each employee can write a part article to the bot and receive a drawing in response.
<ul>
  <li>Drawings are added with the /upload command </li>
  <li>Anyone who has access to the bot can add a file. </li>
  <li>The /delete command to delete drawings (deletes only from the database. the file still remains in the telegram)</li>
  <li>The /list command shows a list of downloaded files with articles.</li>
</p>
</ul>
<h4>For start bot:</h4>
<ul>
  <li>add TOKEN and ADMIN ID (from telegram) in .env file; </li>
  <li>create and activate new venv with aiorgamm and dotenv; </li>
  <li> Start bot - python main.py. </li>
</ul>
</body>
