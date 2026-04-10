import pandas as pd

from random import shuffle

from markdown_pdf import MarkdownPdf, Section

def generate_mcq(questions_bank, output_filename, title, num_questions, questions=None):
    pdf = MarkdownPdf(toc_level=0, optimize=True)
    
    content = ""
    
    content += "**Nom** : " + "&nbsp;" * 40
    content += "**Prénom** : " + "&nbsp;" * 40
    content += "**NOMA** : "
    
    content += """\n"""
    content += "# " + title
    content += """\n"""
    
    content += """
Entourez la lettre correspondante à la bonne réponse. Il n'y a qu'une seule
bonne réponse par question. Blablabla.
    """
    
    if questions is None:
        df = pd.read_excel(questions_bank)
        
        # Replace 'nan' by empty strings ('nan' happens when a question has
        # fewer choices that the others)
        df = df.fillna("")
        
        # Randomly sample one question per category of question to avoid
        # questions on the same topic to be randomly selected, then select n
        # questions among those (note: does not work if less than n categories
        # of questions in the questions bank)
        questions = df.groupby('category').sample().sample(n=num_questions)
    else:
        # Shuffle the questions if questions are provided as an argument
        # (this is usefull if you want the same set of questions to be re-used
        # but shuffle for another version of the test)
        # sample(frac=1) sample all rows without replacement, this is equivalent
        # to shuffling the rows of the DataFrame
        questions = questions.sample(frac=1)
    
    # Begin list of questions
    content += '<ol class="questions">'
    
    for index, row in questions.iterrows():
        # Begin question
        content += "<li>"
        content += "<b>" + row['questions'] + "</b>\n\n"
        
        # Begin list of answers
        content += '<ol class="answers">'

        answers = row[['A', 'B', 'C', 'D']].tolist()

        # Remove empty string from answers
        answers = [a for a in answers if a.strip()]

        if row['keep_last']:
            last_answer = answers[-1]
            answers = answers[0:-1]
        
        shuffle(answers)
    
        for a in answers:
            content += "<li>" + str(a) + "</li>"
                
        if row['keep_last']:
            content += "<li>" + str(last_answer) + "</li>"
    
        # End list of answers
        content += "</ol>"
        
        # End question
        content += "</li>"
    
    # End list of questions
    content += "</ol>"
    
    # Customize the bullet for the answers
    # Switch to none and add ▢ this in the li before for gradescope-ready MCQ
    css = ".questions { font-weight: bold; } .answers { list-style-type: upper-alpha; font-weight: normal;}"
    
    pdf.add_section(Section(content), user_css=css)
    
    pdf.meta["title"] = title
    
    pdf.save(output_filename + ".pdf")
    
    # Return the list of questions to be re-used if needed
    return questions


if __name__ == "__main__":
    questions_bank = 'sample-questions.xlsx'
    
    output_folder = 'PDF/'
    
    # 8 groups, from 1 to 8
    groups = range(1, 9)
    
    for g in groups:
        title = "Le titre de mon QCM"

        # 2 versions per group (A and B), with completely different questions
        generate_mcq(questions_bank=questions_bank,
                     output_filename='PDF/QCM-{0}'.format(g) + 'A',
                     title=title + " ({0}A)".format(g),
                     num_questions=5)
        generate_mcq(questions_bank=questions_bank,
                     output_filename='PDF/QCM-{0}'.format(g) + 'B',
                     title=title + " ({0}A)".format(g),
                     num_questions=5)

        # 2 versions per group (A and B), but we keep the same questions (shuffled) for the two versions
        # questions = generate_mcq(questions_bank=questions_bank,
        #                          output_filename='PDF/QCM-{0}'.format(g) + 'A',
        #                          title=title + " ({0}A)".format(g),
        #                          num_questions=5)
        # generate_mcq(questions_bank=questions_bank,
        #              output_filename='PDF/QCM-{0}'.format(g) + 'B',
        #              title=title + " ({0}A)".format(g),
        #              num_questions=5,
        #              questions=questions)

    
    