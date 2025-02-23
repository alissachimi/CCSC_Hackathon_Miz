import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

programs = [
    ("Major", "Bachelor of Science - Computer Science"),
    ("Major", "Bachelor of Science - Information Technology"),
    ("Major", "Bachelor of Science - Mechanical Engineering")
]

cursor.executemany('''
        INSERT OR IGNORE INTO programs (program_type, name)
        VALUES (?, ?)
    ''', programs)

requirements = [
    ("CMP_SC1050", "Bachelor of Science - Computer Science", 1),
    ("MATH1500", "Bachelor of Science - Computer Science", 1),
    ("CMP_SC2050", "Bachelor of Science - Computer Science", 2),
    ("CMP_SC2270", "Bachelor of Science - Computer Science", 2),
    ("MATH1700", "Bachelor of Science - Computer Science", 2),
    ("CMP_SC3050", "Bachelor of Science - Computer Science", 3),
    ("MATH2300", "Bachelor of Science - Computer Science", 3),
    ("CMP_SC3330", "Bachelor of Science - Computer Science", 4),
    ("CMP_SC3280", "Bachelor of Science - Computer Science", 5),
    ("CMP_SC3380", "Bachelor of Science - Computer Science", 5),
    ("CMP_SC4050", "Bachelor of Science - Computer Science", 6),
    ("CMP_SC4320", "Bachelor of Science - Computer Science", 6),
    ("CMP_SC4520", "Bachelor of Science - Computer Science", 7),
    ("CMP_SC4970W", "Bachelor of Science - Computer Science", 7),
    ("CMP_SC4850", "Bachelor of Science - Computer Science", 8),
    ("CMP_SC4980", "Bachelor of Science - Computer Science", 8),

    ("ENGINR1000", "Bachelor of Science - Information Technology", 1),
    ("INFOTC1040", "Bachelor of Science - Information Technology", 1),
    ("ENGINR1050", "Bachelor of Science - Information Technology", 2),
    ("INFOTC2040", "Bachelor of Science - Information Technology", 2),
    ("INFOTC1610", "Bachelor of Science - Information Technology", 2),
    ("INFOTC2810", "Bachelor of Science - Information Technology", 3),
    ("INFOTC2830", "Bachelor of Science - Information Technology", 4),
    ("INFOTC2910", "Bachelor of Science - Information Technology", 4),
    ("INFOTC3380", "Bachelor of Science - Information Technology", 5),
    ("INFOTC3530", "Bachelor of Science - Information Technology", 5),
    ("INFOTC3650W", "Bachelor of Science - Information Technology", 5),
    ("INFOTC4320", "Bachelor of Science - Information Technology", 6),
    ("INFOTC4970W", "Bachelor of Science - Information Technology", 8),

    ("CHEM1401", "Bachelor of Science - Mechanical Engineering", 1),
    ("MATH1500", "Bachelor of Science - Mechanical Engineering", 1),
    ("ENGINR1000", "Bachelor of Science - Mechanical Engineering", 1),
    ("PHYSCS2750", "Bachelor of Science - Mechanical Engineering", 2),
    ("MATH1700", "Bachelor of Science - Mechanical Engineering", 2),
    ("ENGINR1050", "Bachelor of Science - Mechanical Engineering", 2),
    ("MAE1100", "Bachelor of Science - Mechanical Engineering", 2),
    ("PHYSCS2760", "Bachelor of Science - Mechanical Engineering", 3),
    ("ENGINR1200", "Bachelor of Science - Mechanical Engineering", 3),
    ("ENGINR2100", "Bachelor of Science - Mechanical Engineering", 3),
    ("MATH2300", "Bachelor of Science - Mechanical Engineering", 3),
    ("MAE2510", "Bachelor of Science - Mechanical Engineering", 3),
    ("MAE2300", "Bachelor of Science - Mechanical Engineering", 3),
    ("STAT4710", "Bachelor of Science - Mechanical Engineering", 4),
    ("MATH4100", "Bachelor of Science - Mechanical Engineering", 4),
    ("ENGINR2200", "Bachelor of Science - Mechanical Engineering", 4),
    ("MAE2100", "Bachelor of Science - Mechanical Engineering", 4),
    ("MAE2600", "Bachelor of Science - Mechanical Engineering", 4),
    ("MAE2200W", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3100", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3400", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3500", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3800", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3600", "Bachelor of Science - Mechanical Engineering", 6),
    ("MAE3910", "Bachelor of Science - Mechanical Engineering", 6),
    ("MAE4300", "Bachelor of Science - Mechanical Engineering", 6),
    ("MAE4825", "Bachelor of Science - Mechanical Engineering", 6),
    ("MAE4834", "Bachelor of Science - Mechanical Engineering", 7),
    ("ISE2710", "Bachelor of Science - Mechanical Engineering", 7),
    ("MAE4980W", "Bachelor of Science - Mechanical Engineering", 8),
]

cursor.executemany('''
        INSERT OR IGNORE INTO required_class (class_id, program_name, rec_semester)
        VALUES (?, ?, ?)
    ''', requirements)

electives = [
    # class program name recommended semester level
    ("CMP_SC2830", "Bachelor of Science - Computer Science", 0, 2, "This course focuses on the development of web pages and web applications using Full Stack Development methodologies and tools. Topics such as current events, cloud services, web servers, digital animations, images, audio and video, user interface design, and usability principles are also challenged."),
    ("CMP_SC3530", "Bachelor of Science - Computer Science", 0, 3, "This course is an introduction to UNIX and UNIX-like operating systems and interfaces, to include the file system, command shells, text editors, pipes and filters, input/output system, shell scripting and Regular Expressions. The course will also incorporate an aspect of programming in a UNIX environment, cloud computing, containers and an introduction to System Administration."),
    ("CMP_SC4060", "Bachelor of Science - Computer Science", 0, 4, "This course provides an introduction to algorithms that efficiently compute patterns in strings. Topics covered include basic properties of strings, data structures for processing strings, string decomposition, exact and approximate string matching algorithms."),
    ("CMP_SC4080", "Bachelor of Science - Computer Science", 0, 4, "This course will provide in-depth treatment of the evolution high performance computing architectures and parallel programming techniques for those architectures. We will cover topics such as: multi-process and multi-threaded programming; multi-node system architectures (clusters, grids, and clouds) and distributed programming; and general purpose GPU programming. To reinforce lecture topics, programming projects will be completed using multi-process and multi-threaded techniques for modern multicore, multiprocessor workstations; parallel and distributed programming techniques for modern multi-node systems; and general purpose GPU programming. Parallel algorithms will be investigated, selected, and then developed for various scientific data processing problems. Programming projects will be completed using C and C++ APIs and language extensions, e.g. threads (pthreads, Boost/C++), TBB, CILK, OpenMP, OpenMPI, CUDA and OpenCL."),
    ("CMP_SC4430", "Bachelor of Science - Computer Science", 0, 4, "Introduction to the translation of programming languages by means of interpreters and compilers. Lexical analysis, syntax specification, parsing, error-recovery, syntax-directed translation, semantic analysis, symbol tables for block structured languages, and run-time storage organization. May not be counted toward Computer Science MS/PHD."),
    ("CMP_SC4530", "Bachelor of Science - Computer Science", 0, 4, "This course covers principles that integrate computing theories and information technologies with the design, programming and application of distributed systems. The course topics will familiarize students with distributed system models and enabling technologies; virtual machines and virtualization of clusters, networks and data centers; cloud platform architecture with security over virtualized data centers; service- oriented architectures for distributed computing; and cloud programming and software environments. Additionally, students will learn how to conduct some parallel and distributed programming and performance evaluation experiments on applications within available cloud platforms. Finally we will survey research literature and latest technology trends that are shaping the future of high performance, distributed and cloud computing."),
    ("CMP_SC4650", "Bachelor of Science - Computer Science", 0, 4, "Fundamentals of digital image processing hardware and software including digital image acquisition, image display, image enhancement, image transforms and segmentation."),
    ("CMP_SC4630", "Bachelor of Science - Computer Science", 0, 4, "The course focuses on rapid game prototyping and development utilizing the Unity game engine and C#. tools. You will learn the fundamentals of game programming and also a platform which is actually used t to make published games across multiple platforms (Mac, PC, web, iOS, Android etc)."),
    ("CMP_SC4750", "Bachelor of Science - Computer Science", 0, 4, "This course is intended to be a general introduction to the field of Artificial Intelligence (AI). It will provide exposure to a range of core AI topics including intelligent agent, problem solving by search and game playing, constraint satisfaction problems, propositional and first-order logic, probability in AI, and machine learning. The topics covered in this course are closely related to the common core of Computing & Information education -- about C&I know-how and the ways of thinking and problem solving that characterize C&I community: a system view of the world, a focus on mathematical and computational representation of systems, information representation and transformation, and so forth."),

    ("INFOTC2610", "Bachelor of Science - Information Technology", 0, 2, "This project-based course addresses the fundamentals of design, digital media, and creative technologies. You will examine and utilize current technologies and standards within the digital media industry, including the software, hardware, and techniques needed to capture, store, manipulate, and deliver digital media. Through hands-on experience, you will achieve an understanding of pre-production, production, and post-production concepts, such as non-linear editing workflows, project management, narrative story structures, image composition and aesthetics, audio and video capture techniques, color theories and processing, computer components and editing hardware, intellectual property rights, addressing a target audience, industry trends, and more. The course also provides guidance on establishing and bolstering competencies in critical problem solving, teamwork, time management, networking, and conflict resolution."),
    ("INFOTC2615", "Bachelor of Science - Information Technology", 0, 2, "This project-based course is an intensive study of design and color processing for digital video. The course introduces advanced technologies and standards within the digital media industry, including the software, hardware, and techniques needed to capture, store, manipulate, and deliver digital media. Through an asynchronous experience, you will improve your understanding of color engineering concepts, such as post-production workflows, project management, color correcting and grading, color theories and science, color management systems, camera and sensor systems, computer components and editing hardware, display technologies, digital broadcasting requirements and signal constraints, peripherals, and more. The course also provides guidance on establishing and bolstering competencies in critical problem solving, teamwork, time management, networking, and conflict resolution."),
    ("INFOTC2620", "Bachelor of Science - Information Technology", 0, 2, "Students will investigate digital modeling and animation with an emphasis on principles. The skills and workflows that students learn within this class can be transferred to other software used within the industry with minor differences. This is a project-based course where students will be completing projects to show that they have mastery of the provided learning objectives. By the end of the class, students will be able to design and create unique digital models, environments, and animations."),
    ("INFOTC2630", "Bachelor of Science - Information Technology", 0, 2, "Students will develop foundational skills in game design and theory, and become proficient in the tools used to develop conceptual gaming environments. The student will develop skills to discuss, develop, and demonstrate the design process in cooperation with current game theories and practices. The student will develop collaborative and cooperative design techniques mirroring that of the industry."),
    ("INFOTC3630", "Bachelor of Science - Information Technology", 0, 3, "The course will provide students with a good understanding of the fundamentals of virtual reality and practical hands on VR experience development skills. It will introduce students to the software, hardware, and concepts involved with the current state of the art in virtual reality. This course will focus on using the recent consumer-grade equipment to design and construct virtual environment and experience."),
    ("INFOTC3640", "Bachelor of Science - Information Technology", 0, 3, "This advanced media creation course is an introduction to the fundamentals of motion graphic design, 2-D animation, and visual effects design for content and new media creation. It is a project-based course that requires understanding of NLEs, experience in media creation and design, understanding of basic audio/video compression, and understanding of basic media design and concepts. Computer programs designed for graphic design, motion graphics, 2-D animation, and visual effects are integrated throughout the course."),
    ("INFOTC3660", "Bachelor of Science - Information Technology", 0, 3, "This course is an intensive study of the techniques and art behind the use of audio in today's media design environments. From the theater to television, from tablet and mobile device to computer, this course will focus on the four major sound design areas: sound in cinema, sound creation, sound manipulation, and environmental sound layering."),
    ("INFOTC3810", "Bachelor of Science - Information Technology", 0, 3, "This course covers principles of networking configuration and security authentication, IP security, network management security, wireless security, and system security by studying attacks on computer systems, network, and the Web as well as detection and prevention. Work is completed in Unix/Linux environments and in Microsoft Windows environment. Students will need to setup a virtual private infrastructure to perform multiple tasks; additionally unlimited AWS cloud resources will be available for them. The course emphasizes 'learning by doing' and has a 90% hands-on and 10% theory. Much of this information consists of skills and abilities that employers want and expect in the real world of IT - in a small to medium size organization."),
    ("INFOTC4410", "Bachelor of Science - Information Technology", 0, 4, "This is the first in a series of courses on developing Android applications using Android Studio and the Java and Kotlin programming languages."),
    ("INFOTC4405", "Bachelor of Science - Information Technology", 0, 4, "This is a first in a series of courses on developing iOS applications using Xcode, and the Swift programming language on the macOS platform.")
]

cursor.executemany('''
        INSERT OR IGNORE INTO elective_class (class_id, program_name, rec_semester, level, description)
        VALUES (?, ?, ?, ?, ?)
    ''', electives)

conn.commit()
conn.close()
print("Database updated successfully!")