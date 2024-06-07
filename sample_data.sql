-- Start by deleting answers since they depend on questions
DELETE FROM single_choice_answer;

DELETE FROM multiple_choice_answer;

DELETE FROM open_answer;

DELETE FROM assignment_answer;

DELETE FROM gap_text_answer;

-- Next, delete options as they depend on questions
DELETE FROM single_choice_option;

DELETE FROM multiple_choice_option;

DELETE FROM open_option;

DELETE FROM assignment_option;

DELETE FROM gap_text_option;

-- Then, delete sub-questions for gap text questions
DELETE FROM gap_text_sub_question;

-- Delete all questions
DELETE FROM single_choice_question;

DELETE FROM multiple_choice_question;

DELETE FROM open_question;

DELETE FROM assignment_question;

DELETE FROM gap_text_question;

-- Finally, delete the quizzes
DELETE FROM quiz;

-- Create a new quiz about Clean Code
INSERT INTO quiz (title) VALUES ('Clean Code Essentials');

-- Assuming the quiz was inserted with an ID of 1, create the single choice question
INSERT INTO
    single_choice_question (
        title,
        "text",
        "index",
        quiz_id,
        correct_index
    )
VALUES (
        'What principle promotes readability?',
        'Choose the principle that best promotes code readability.',
        1,
        1,
        2
    );

-- Insert options for the single choice question (assuming the question has an ID of 1)
INSERT INTO
    single_choice_option ("text", "index", question_id)
VALUES ('DRY Principle', 1, 1),
    ('KISS Principle', 2, 1),
    ('YAGNI Principle', 3, 1),
    ('SOLID Principle', 4, 1);

-- -- Create the multiple choice question
-- INSERT INTO
--     multiple_choice_question (
--         title,
--         "text",
--         "index",
--         quiz_id,
--         correct_indices
--     )
-- VALUES (
--         'Which practices are recommended for clean code?',
--         'Select all that apply.',
--         2,
--         1,
--         '[1, 3, 4]'
--     );

-- -- Insert options for the multiple choice question (assuming the question has an ID of 2)
-- INSERT INTO
--     multiple_choice_option ("text", "index", question_id)
-- VALUES (
--         'Using meaningful names',
--         1,
--         2
--     ),
--     ('Skipping code reviews', 2, 2),
--     ('Refactoring regularly', 3, 2),
--     ('Writing unit tests', 4, 2);
