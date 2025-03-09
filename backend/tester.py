dat = [
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.1: Introduction",
		"url": "https://www.youtube.com/watch?v=8ndsDXohLMQ"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.2: Introduction to Replit",
		"url": "https://www.youtube.com/watch?v=NgZZ0HIUqbs"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.3: More on Replit, print and Common Mistakes",
		"url": "https://www.youtube.com/watch?v=As7_aq6XGfI"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.4: A Quick Introduction to Variables",
		"url": "https://www.youtube.com/watch?v=Yg6xzi2ie5s"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.5: Variables and Input Statement",
		"url": "https://www.youtube.com/watch?v=ruQb8jzkGyQ"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.6: Variables and Literals",
		"url": "https://www.youtube.com/watch?v=tDaXdoKfX0k"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.7: Data Types 1",
		"url": "https://www.youtube.com/watch?v=8n4MBjuDBu4"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.8: Data Types 2",
		"url": "https://www.youtube.com/watch?v=xQXxufhEJHw"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.9: Operators and Expressions 1",
		"url": "https://www.youtube.com/watch?v=8pu73HKzNOE"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.10: Operators and Expressions 2",
		"url": "https://www.youtube.com/watch?v=Y53K9FFu97Q"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.11: Introduction to Strings",
		"url": "https://www.youtube.com/watch?v=sS89tiDuqoM"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.12: More on Strings",
		"url": "https://www.youtube.com/watch?v=e45MVXwya7A"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.13: Conclusion: FAQs",
		"url": "https://www.youtube.com/watch?v=_Ccezy5hlc8"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.1: Introduction",
		"url": "https://www.youtube.com/watch?v=aEPFZSzZ6VQ"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.2: Variables : A Programmer's Perspective",
		"url": "https://www.youtube.com/watch?v=XZSnqseRbZY"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.3: Variables Revisited: Dynamic Typing",
		"url": "https://www.youtube.com/watch?v=2OFZY77eOjw"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.4: More on Variables, Operators and Expressions",
		"url": "https://www.youtube.com/watch?v=-f833WH_cVo"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.5: Escape characters and types of quotes",
		"url": "https://www.youtube.com/watch?v=4vWM2oTGEio"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.6: String Methods",
		"url": "https://www.youtube.com/watch?v=bRAo6TJJjCU"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.7: An Interesting Cipher: More on Strings",
		"url": "https://www.youtube.com/watch?v=oxFYdHVNpg8"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.8: Introduction to the if statement",
		"url": "https://www.youtube.com/watch?v=FTX5wF_3J9Q"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.9: Tutorial on if, else and else-if (elif) conditions",
		"url": "https://www.youtube.com/watch?v=-dBqiRCHbNw"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.10: Introduction to 'import library'",
		"url": "https://www.youtube.com/watch?v=OdjXL5U95eI"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.11: Different ways to import a library",
		"url": "https://www.youtube.com/watch?v=eW58_ky7oc8"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.12: Conclusion",
		"url": "https://www.youtube.com/watch?v=DK16M8EvOLE"
	}
]


from application.ai import ink
from application.fs import FileManager

python = FileManager('sub')
aisum = FileManager('aisum')
aisum.create_directory()

print()

for i in python.files_in_dir():
    fn = i
    cont = python.file_to_text(fn)
    res = ink.summarize({
        "prompt" : "",
        "content" : cont
    })
    print()
    aisum.text_to_file(fn, res['summary'])
    