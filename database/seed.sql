-- SkillMatch Sample/Demo Data
-- NOTE: All companies, opportunities and apply URLs below are SAMPLE DATA
-- created for hackathon demonstration purposes only. They are not verified
-- real listings. Replace with real, verified postings before production use.

USE skillmatch;

-- ==========================
-- SKILLS (20+)
-- ==========================
INSERT INTO skills (skill_name) VALUES
('Python'),('SQL'),('HTML'),('CSS'),('JavaScript'),('React'),('Node.js'),
('Flask'),('Django'),('Java'),('C++'),('Git'),('Docker'),('AWS'),
('Machine Learning'),('Data Analysis'),('MongoDB'),('MySQL'),('REST APIs'),
('Bootstrap'),('TypeScript'),('Linux'),('Cybersecurity Basics'),('Excel');

-- ==========================
-- COMPANIES (10, sample/demo)
-- ==========================
INSERT INTO companies (company_name, website, is_verified) VALUES
('NovaTech Labs', 'https://example.com/novatech', FALSE),
('BrightPath Solutions', 'https://example.com/brightpath', FALSE),
('CloudNine Systems', 'https://example.com/cloudnine', FALSE),
('DataSphere Analytics', 'https://example.com/datasphere', FALSE),
('PixelForge Studios', 'https://example.com/pixelforge', FALSE),
('SecureNet Technologies', 'https://example.com/securenet', FALSE),
('GreenLeaf Fintech', 'https://example.com/greenleaf', FALSE),
('Orbit Commerce', 'https://example.com/orbit', FALSE),
('Quantum Byte', 'https://example.com/quantumbyte', FALSE),
('Skyline Ventures', 'https://example.com/skyline', FALSE);

-- ==========================
-- OPPORTUNITIES (20, sample/demo, is_sample=TRUE)
-- ==========================
INSERT INTO opportunities (company_id, title, type, description, location, work_mode, stipend, salary, education_requirement, experience_requirement, deadline, apply_url, is_sample) VALUES
(1, 'Frontend Developer Intern', 'Internship', 'Work on React-based dashboards for our SaaS product.', 'Bangalore', 'Remote', 15000, 0, 'BCA/B.Tech', '0-1 years', '2026-11-30', 'https://example.com/apply/novatech-frontend', TRUE),
(1, 'Backend Developer Intern', 'Internship', 'Build REST APIs using Python and Flask.', 'Bangalore', 'Hybrid', 18000, 0, 'BCA/B.Tech', '0-1 years', '2026-12-05', 'https://example.com/apply/novatech-backend', TRUE),
(2, 'Full Stack Developer (Entry Level)', 'Full-time Job', 'Join our engineering team building MERN stack products.', 'Pune', 'On-site', 0, 480000, 'B.Tech/BCA', '0-2 years', '2026-11-20', 'https://example.com/apply/brightpath-fullstack', TRUE),
(2, 'Junior QA Engineer', 'Full-time Job', 'Manual and automated testing for web applications.', 'Pune', 'Hybrid', 0, 350000, 'Any Graduate', '0-1 years', '2026-11-25', 'https://example.com/apply/brightpath-qa', TRUE),
(3, 'Cloud Support Intern', 'Internship', 'Assist with AWS infrastructure monitoring and support.', 'Hyderabad', 'Remote', 12000, 0, 'B.Tech/BCA', '0-1 years', '2026-12-10', 'https://example.com/apply/cloudnine-support', TRUE),
(3, 'DevOps Intern', 'Internship', 'Work with Docker, CI/CD pipelines and deployment automation.', 'Hyderabad', 'On-site', 20000, 0, 'B.Tech/BCA', '0-1 years', '2026-12-15', 'https://example.com/apply/cloudnine-devops', TRUE),
(4, 'Data Analyst Intern', 'Internship', 'Analyze business data using SQL and Python.', 'Mumbai', 'Hybrid', 15000, 0, 'Any Graduate', '0-1 years', '2026-11-28', 'https://example.com/apply/datasphere-analyst', TRUE),
(4, 'Machine Learning Intern', 'Internship', 'Build and evaluate ML models for prediction tasks.', 'Mumbai', 'Remote', 20000, 0, 'B.Tech/BCA/MCA', '0-1 years', '2026-12-01', 'https://example.com/apply/datasphere-ml', TRUE),
(5, 'UI/UX Design Intern', 'Internship', 'Design responsive interfaces using Figma and CSS.', 'Delhi', 'Remote', 10000, 0, 'Any Graduate', '0-1 years', '2026-11-22', 'https://example.com/apply/pixelforge-uiux', TRUE),
(5, 'Web Developer (Part-time)', 'Part-time', 'Maintain and update client websites using HTML/CSS/JS.', 'Delhi', 'Remote', 8000, 0, 'Any Graduate', '0-1 years', '2026-11-18', 'https://example.com/apply/pixelforge-webdev', TRUE),
(6, 'Cybersecurity Intern', 'Internship', 'Assist with vulnerability assessments and security audits.', 'Bangalore', 'On-site', 18000, 0, 'B.Tech/BCA', '0-1 years', '2026-12-20', 'https://example.com/apply/securenet-cyber', TRUE),
(6, 'Security Analyst (Entry Level)', 'Full-time Job', 'Monitor systems for security threats and incidents.', 'Bangalore', 'Hybrid', 0, 420000, 'B.Tech/BCA', '0-1 years', '2026-12-18', 'https://example.com/apply/securenet-analyst', TRUE),
(7, 'Software Engineer Apprentice', 'Apprenticeship', 'Structured apprenticeship program covering full stack development.', 'Chennai', 'On-site', 16000, 0, 'Any Graduate', '0-1 years', '2026-11-27', 'https://example.com/apply/greenleaf-apprentice', TRUE),
(7, 'Python Developer Intern', 'Internship', 'Build backend services and automation scripts.', 'Chennai', 'Remote', 15000, 0, 'B.Tech/BCA', '0-1 years', '2026-12-08', 'https://example.com/apply/greenleaf-python', TRUE),
(8, 'E-commerce Backend Intern', 'Internship', 'Work on order management APIs with Node.js.', 'Noida', 'Hybrid', 14000, 0, 'B.Tech/BCA', '0-1 years', '2026-11-24', 'https://example.com/apply/orbit-backend', TRUE),
(8, 'Junior Software Developer', 'Full-time Job', 'Develop and maintain internal tools using React and Flask.', 'Noida', 'On-site', 0, 400000, 'B.Tech/BCA', '0-2 years', '2026-12-02', 'https://example.com/apply/orbit-junior-dev', TRUE),
(9, 'Database Intern', 'Internship', 'Design and optimize MySQL databases for internal apps.', 'Kolkata', 'On-site', 12000, 0, 'B.Tech/BCA', '0-1 years', '2026-11-29', 'https://example.com/apply/quantumbyte-db', TRUE),
(9, 'Software Development Intern', 'Internship', 'General SDE internship covering full stack tasks.', 'Kolkata', 'Remote', 15000, 0, 'B.Tech/BCA', '0-1 years', '2026-12-12', 'https://example.com/apply/quantumbyte-sde', TRUE),
(10, 'Associate Software Engineer', 'Full-time Job', 'Entry level role building products with React and Node.js.', 'Remote', 'Remote', 0, 450000, 'B.Tech/BCA/MCA', '0-1 years', '2026-12-22', 'https://example.com/apply/skyline-associate', TRUE),
(10, 'Technical Support Intern', 'Internship', 'Provide first-line technical support and bug triage.', 'Remote', 'Remote', 10000, 0, 'Any Graduate', '0-1 years', '2026-11-19', 'https://example.com/apply/skyline-support', TRUE);

-- ==========================
-- OPPORTUNITY SKILLS MAPPING
-- ==========================
INSERT INTO opportunity_skills (opportunity_id, skill_id) VALUES
(1,3),(1,4),(1,5),(1,6),(1,20),
(2,1),(2,2),(2,8),(2,19),
(3,5),(3,6),(3,7),(3,8),(3,18),
(4,1),(4,2),(4,18),
(5,14),(5,12),(5,22),
(6,13),(6,12),(6,22),(6,1),
(7,1),(7,2),(7,24),
(8,1),(8,15),(8,16),
(9,3),(9,4),(9,20),
(10,3),(10,4),(10,5),
(11,23),(11,22),(11,2),
(12,23),(12,22),(12,1),
(13,1),(13,2),(13,3),(13,4),(13,5),
(14,1),(14,12),(14,19),
(15,7),(15,5),(15,18),
(16,5),(16,6),(16,8),
(17,2),(17,18),(17,12),
(18,1),(18,2),(18,3),(18,4),(18,5),
(19,5),(19,6),(19,7),(19,18),
(20,3),(20,4),(20,20);
