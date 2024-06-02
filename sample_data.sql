-- clear all tables except user and token tables
DELETE FROM single_choice_option;

DELETE FROM multiple_choice_option;

DELETE FROM single_choice_question;

DELETE FROM multiple_choice_question;

DELETE FROM quiz;

DELETE FROM "result";

DELETE FROM open_question;

DELETE FROM open_option;

DELETE FROM assignment_question;

DELETE FROM assignment_option;

DELETE FROM gap_text_question;

DELETE FROM gap_text_option;

DELETE FROM gap_text_sub_question;

-- Insert a quiz
INSERT INTO quiz (title) VALUES ('Clean Code Principles');

-- Get the ID of the inserted quiz
-- Assuming it's 1 if it's the first entry (otherwise use SELECT to find the right ID)

-- Insert single choice questions and options
INSERT INTO
    single_choice_question (
        quiz_id,
        title,
        "text",
        "index"
    )
VALUES (
        1,
        'Single Responsibility Principle',
        'What does the Single Responsibility Principle advocate?',
        1
    );

INSERT INTO
    single_choice_option (
        question_id,
        "text",
        is_correct,
        "index"
    )
VALUES (
        1,
        'One class should have only one reason to change.',
        1,
        1
    );

INSERT INTO
    single_choice_option (
        question_id,
        "text",
        is_correct,
        "index"
    )
VALUES (
        1,
        'Every class should be able to perform multiple functions.',
        0,
        2
    );

INSERT INTO
    single_choice_option (
        question_id,
        "text",
        is_correct,
        "index"
    )
VALUES (
        1,
        'Classes should be open for extension but closed for modification.',
        0,
        3
    );

-- Insert multiple choice questions and options
INSERT INTO
    multiple_choice_question (
        quiz_id,
        title,
        "text",
        "index"
    )
VALUES (
        1,
        'Benefits of Clean Code',
        'Which of the following are benefits of clean code?',
        2
    );

INSERT INTO
    multiple_choice_option (
        question_id,
        "text",
        is_correct,
        "index"
    )
VALUES (1, 'Easier to modify', 1, 1);

INSERT INTO
    multiple_choice_option (
        question_id,
        "text",
        is_correct,
        "index"
    )
VALUES (
        1,
        'Requires less testing',
        0,
        2
    );

INSERT INTO
    multiple_choice_option (
        question_id,
        "text",
        is_correct,
        "index"
    )
VALUES (1, 'More readable', 1, 3);

INSERT INTO
    multiple_choice_option (
        question_id,
        "text",
        is_correct,
        "index"
    )
VALUES (
        1,
        'Faster execution time',
        0,
        4
    );
