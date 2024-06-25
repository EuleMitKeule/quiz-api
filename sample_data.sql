-- Clear existing data
DELETE FROM single_choice_answer;

DELETE FROM multiple_choice_answer;

DELETE FROM open_answer;

DELETE FROM assignment_answer;

DELETE FROM gap_text_answer;

DELETE FROM single_choice_option;

DELETE FROM multiple_choice_option;

DELETE FROM open_option;

DELETE FROM assignment_option;

DELETE FROM gap_text_option;

DELETE FROM gap_text_sub_question;

DELETE FROM single_choice_question;

DELETE FROM multiple_choice_question;

DELETE FROM open_question;

DELETE FROM assignment_question;

DELETE FROM gap_text_question;

DELETE FROM quiz_label_relation;

DELETE FROM quiz;

DELETE FROM label;

-- Create labels
INSERT INTO
    label (id, text)
VALUES (1, 'Software Development'),
    (2, 'Best Practices'),
    (3, 'Advanced Topics'),
    (4, 'Testing Techniques'),
    (5, 'Project Management');

-- Create quizzes
INSERT INTO
    quiz (id, title)
VALUES (1, 'Clean Code Essentials'),
    (
        2,
        'Advanced Software Patterns'
    ),
    (
        3,
        'Effective Testing Strategies'
    ),
    (4, 'Agile Project Management'),
    (5, 'DevOps Principles');

-- Quiz and Label Relations
INSERT INTO
    quiz_label_relation (quiz_id, label_id)
VALUES (1, 1),
    (1, 2),
    (2, 1),
    (2, 3),
    (3, 1),
    (3, 4),
    (4, 1),
    (4, 5),
    (5, 1),
    (5, 5);

-- Questions and options for first quiz (Clean Code Essentials)
-- Single choice questions
INSERT INTO
    single_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_index,
        difficulty
    )
VALUES (
        1,
        'What principle promotes readability?',
        'Choose the principle that best promotes code readability.',
        0,
        1,
        1,
        'EASY'
    ),
    (
        2,
        'What does SOLID stand for?',
        'Identify what the SOLID acronym stands for in object-oriented design.',
        1,
        1,
        4,
        'MEDIUM'
    );

INSERT INTO
    single_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (1, 'DRY Principle', 0, 1),
    (2, 'KISS Principle', 1, 1),
    (3, 'YAGNI Principle', 2, 1),
    (4, 'SOLID Principle', 3, 1),
    (
        5,
        'Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion',
        0,
        2
    ),
    (
        6,
        'Simple, Observable, Logical, Integrated, Dynamic',
        1,
        2
    ),
    (
        7,
        'Structured, Observable, Logical, Inclusive, Diverse',
        2,
        2
    );

-- Multiple choice question
INSERT INTO
    multiple_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_indices,
        difficulty
    )
VALUES (
        3,
        'Which practices are recommended for clean code?',
        'Select all that apply.',
        2,
        1,
        '[0, 2, 3]',
        'MEDIUM'
    );

INSERT INTO
    multiple_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (
        8,
        'Using meaningful names',
        0,
        3
    ),
    (
        9,
        'Skipping code reviews',
        1,
        3
    ),
    (
        10,
        'Refactoring regularly',
        2,
        3
    ),
    (
        11,
        'Writing unit tests',
        3,
        3
    );

-- Extending other quizzes
-- Advanced Software Patterns
INSERT INTO
    multiple_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_indices,
        difficulty
    )
VALUES (
        4,
        'Patterns for high scalability',
        'Which patterns enhance system scalability?',
        0,
        2,
        '[1, 3]',
        'HARD'
    );

INSERT INTO
    multiple_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (12, 'Singleton', 0, 4),
    (13, 'Observer', 1, 4),
    (14, 'Decorator', 2, 4),
    (15, 'CQRS', 3, 4);

-- Effective Testing Strategies
INSERT INTO
    single_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_index,
        difficulty
    )
VALUES (
        5,
        'Best practice for unit testing?',
        'What is considered best practice when writing unit tests?',
        0,
        3,
        1,
        'EASY'
    );

INSERT INTO
    single_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (
        16,
        'Test internal implementation',
        0,
        5
    ),
    (
        17,
        'Test against public interfaces',
        1,
        5
    ),
    (
        18,
        'Test only on production',
        2,
        5
    ),
    (
        19,
        'Avoid testing getters and setters',
        3,
        5
    );

-- More data for Agile Project Management and DevOps Principles can be similarly created.
-- Continue creating more quizzes
-- Cloud Computing Fundamentals
INSERT INTO
    quiz (id, title)
VALUES (
        6,
        'Cloud Computing Fundamentals'
    );

-- Database Management Systems
INSERT INTO
    quiz (id, title)
VALUES (
        7,
        'Database Management Systems'
    );

-- Software Security Essentials
INSERT INTO
    quiz (id, title)
VALUES (
        8,
        'Software Security Essentials'
    );

-- Quiz and Label Relations for new quizzes
INSERT INTO
    quiz_label_relation (quiz_id, label_id)
VALUES (6, 1),
    (6, 3),
    (7, 1),
    (7, 2),
    (8, 1),
    (8, 2);

-- Questions and options for Cloud Computing Fundamentals
-- Single choice question
INSERT INTO
    single_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_index,
        difficulty
    )
VALUES (
        6,
        'Which service model provides the most control over your environment?',
        'Select the cloud service model that offers the most control.',
        0,
        6,
        2,
        'MEDIUM'
    );

INSERT INTO
    single_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (
        20,
        'Software as a Service (SaaS)',
        0,
        6
    ),
    (
        21,
        'Platform as a Service (PaaS)',
        1,
        6
    ),
    (
        22,
        'Infrastructure as a Service (IaaS)',
        2,
        6
    );

-- Multiple choice question
INSERT INTO
    multiple_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_indices,
        difficulty
    )
VALUES (
        7,
        'Which are core benefits of cloud computing?',
        'Select all correct answers.',
        1,
        6,
        '[0, 2, 3]',
        'EASY'
    );

INSERT INTO
    multiple_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (23, 'Scalability', 0, 7),
    (
        24,
        'Higher initial costs',
        1,
        7
    ),
    (25, 'Disaster recovery', 2, 7),
    (26, 'Flexibility', 3, 7);

-- Questions and options for Database Management Systems
-- Single choice question
INSERT INTO
    single_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_index,
        difficulty
    )
VALUES (
        8,
        'What is ACID in databases?',
        'What does the ACID acronym stand for in database management?',
        0,
        7,
        0,
        'MEDIUM'
    );

INSERT INTO
    single_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (
        27,
        'Atomicity, Consistency, Isolation, Durability',
        0,
        8
    ),
    (
        28,
        'Association, Consistency, Integrity, Durability',
        1,
        8
    ),
    (
        29,
        'Atomicity, Completeness, Integrity, Dependability',
        2,
        8
    );

-- Questions and options for Software Security Essentials
-- Multiple choice question
INSERT INTO
    multiple_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_indices,
        difficulty
    )
VALUES (
        9,
        'Which practices improve software security?',
        'Select all that apply.',
        0,
        8,
        '[0, 1, 3]',
        'HARD'
    );

INSERT INTO
    multiple_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (
        30,
        'Regular security audits',
        0,
        9
    ),
    (
        31,
        'Frequent password updates',
        1,
        9
    ),
    (
        32,
        'Using outdated software',
        2,
        9
    ),
    (
        33,
        'Implementing encryption',
        3,
        9
    );

-- Additional questions and quizzes can be similarly created.
-- Machine Learning Fundamentals
INSERT INTO
    quiz (id, title)
VALUES (
        9,
        'Machine Learning Fundamentals'
    );

-- Linking quiz to labels
INSERT INTO
    quiz_label_relation (quiz_id, label_id)
VALUES (9, 1),
    (9, 3);

-- Questions and options for Machine Learning Fundamentals
-- Single choice question on basic concepts
INSERT INTO
    single_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_index,
        difficulty
    )
VALUES (
        10,
        'Which algorithm is best for non-linear data?',
        'Choose the algorithm that is most suitable for non-linear data.',
        0,
        9,
        2,
        'MEDIUM'
    );

INSERT INTO
    single_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (
        34,
        'Linear Regression',
        0,
        10
    ),
    (35, 'Decision Trees', 1, 10),
    (
        36,
        'K-Means Clustering',
        2,
        10
    );

-- Multiple choice question on model evaluation
INSERT INTO
    multiple_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_indices,
        difficulty
    )
VALUES (
        11,
        'What are common metrics to evaluate a classification model?',
        'Select all that apply.',
        1,
        9,
        '[0, 1, 3]',
        'HARD'
    );

INSERT INTO
    multiple_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (37, 'Accuracy', 0, 11),
    (
        38,
        'Mean Squared Error',
        1,
        11
    ),
    (39, 'R-squared', 2, 11),
    (
        40,
        'Precision and Recall',
        3,
        11
    );

-- Single choice question on deep learning
INSERT INTO
    single_choice_question (
        id,
        title,
        "text",
        "index",
        quiz_id,
        correct_index,
        difficulty
    )
VALUES (
        12,
        'Which layer type is commonly used in CNNs?',
        'Identify the layer most commonly associated with Convolutional Neural Networks.',
        2,
        9,
        0,
        'EASY'
    );

INSERT INTO
    single_choice_option (
        id,
        "text",
        "index",
        question_id
    )
VALUES (
        41,
        'Convolutional layer',
        0,
        12
    ),
    (42, 'Recurrent layer', 1, 12),
    (43, 'Dense layer', 2, 12);

-- Additional quizzes on specific machine learning techniques or applications can be similarly created.

-- Add a new quiz
INSERT INTO
    quiz ("id", title)
VALUES (
        10,
        'Real-Time Systems Essentials'
    );

-- Link to labels
INSERT INTO
    quiz_label_relation (quiz_id, label_id)
VALUES (10, 1),
    (10, 2);
-- Single choice question
INSERT INTO
    single_choice_question (
        "id",
        title,
        "text",
        "index",
        quiz_id,
        correct_index,
        difficulty
    )
VALUES (
        13,
        'What is a key characteristic of real-time systems?',
        'Select the most accurate description.',
        0,
        10,
        0,
        'EASY'
    );

-- Options for the question
INSERT INTO
    single_choice_option (
        "id",
        "text",
        "index",
        question_id
    )
VALUES (44, 'Predictability', 0, 13),
    (45, 'Scalability', 1, 13),
    (46, 'Flexibility', 2, 13);

-- Multiple choice question
INSERT INTO
    multiple_choice_question (
        "id",
        title,
        "text",
        "index",
        quiz_id,
        correct_indices,
        difficulty
    )
VALUES (
        14,
        'Which are critical features of a real-time operating system?',
        'Select all that apply.',
        1,
        10,
        '[0, 2]',
        'MEDIUM'
    );

-- Options for the question
INSERT INTO
    multiple_choice_option (
        "id",
        "text",
        "index",
        question_id
    )
VALUES (
        47,
        'Deterministic performance',
        0,
        14
    ),
    (
        48,
        'Multi-user support',
        1,
        14
    ),
    (
        49,
        'Minimal interrupt latency',
        2,
        14
    );
-- Single choice question
INSERT INTO
    single_choice_question (
        "id",
        title,
        "text",
        "index",
        quiz_id,
        correct_index,
        difficulty
    )
VALUES (
        15,
        'Which Agile methodology emphasizes flexibility?',
        'Choose the Agile methodology that best emphasizes adaptability and change.',
        0,
        4,
        1,
        'MEDIUM'
    );

-- Options for the question
INSERT INTO
    single_choice_option (
        "id",
        "text",
        "index",
        question_id
    )
VALUES (50, 'Scrum', 0, 15),
    (51, 'Kanban', 1, 15),
    (52, 'Waterfall', 2, 15);
-- Multiple choice question
INSERT INTO
    multiple_choice_question (
        "id",
        title,
        "text",
        "index",
        quiz_id,
        correct_indices,
        difficulty
    )
VALUES (
        16,
        'Key DevOps practices?',
        'Select all that apply to core DevOps practices.',
        0,
        5,
        '[0, 1, 2]',
        'EASY'
    );

INSERT INTO
    multiple_choice_option (
        "id",
        "text",
        "index",
        question_id
    )
VALUES (
        53,
        'Continuous integration',
        0,
        16
    ),
    (
        54,
        'Automated deployments',
        1,
        16
    ),
    (55, 'Manual testing', 2, 16),
    (56, 'Yearly planning', 3, 16);
