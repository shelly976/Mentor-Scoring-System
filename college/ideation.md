# Mentor Scoring System – Ideation Document

## 1. Overview
This project ranks mentors based on multiple performance indicators including student progress, responsiveness, engagement, and feedback quality. The goal is to produce a fair, normalized, and weighted mentor score that can be used to rank mentors objectively.

The final mentor score combines four components:

- **Progress Score (P)**  
- **Responsiveness Score (R)**  
- **Engagement Score (E)**  
- **Feedback Score (F)**  

Weights are applied to reflect the relative importance of each factor.

---

## 2. Scoring Functions

### 2.1 Progress Score `P`
Measures the average milestone completion of students under a mentor:

P = (Sum of (MilestonesCompleted / TotalMilestones) for all students) / Number of Students

- **Normalization:** To compare across mentors, raw progress scores are scaled to [0,1]:


- **Rationale:** Ensures that mentors with consistently high-performing students are rewarded.  

---

### 2.2 Responsiveness Score `R`
We use an exponential decay function to penalize slow response times:

R = exp(-h * tavg)

Where:

- tavg = average response time in hours  
- h = 0.1 (controls strictness of penalty)  

**Rationale:** Fast responses are rewarded, slow responses are penalized exponentially. The decay ensures that extreme delays significantly reduce the score.

---

### 2.3 Engagement Score `E`
Engagement measures how actively a mentor participates in meetings, code reviews, and messaging:

E = w_meetings * Meetings + w_reviews * CodeReviews + w_messages * Messages

E_norm = (E - E_min) / (E_max - E_min)


**Rationale:** Balances quantity and quality of mentor engagement. Normalization ensures fair comparison across mentors with different volumes of activity.

---

### 2.4 Feedback Score `F`
Feedback from mentees is normalized to reduce bias from extreme ratings:

1. Clip ratings to [1.5, 4.5] to reduce unfair low/high feedback.  
2. Compute the mean per mentor:

F = mean(clipped ratings)   


3. Normalize across mentors:
F_norm = (F - F_min) / (F_max - F_min)


**Rationale:** Reduces the impact of extreme or unfair feedback while rewarding consistently good feedback.

---

## 3. Weighted Mentor Score

The final mentor score is computed as:

The final mentor score is computed as:

Score = w_P * P_norm + w_R * R + w_E * E_norm + w_F * F_norm


Where the weights reflect the importance of each metric:

- w_P = 0.40 (Progress)  
- w_R = 0.25 (Responsiveness)  
- w_E = 0.20 (Engagement)  
- w_F = 0.15 (Feedback)  

**Rationale:** Progress is most critical, followed by responsiveness. Engagement and feedback are still important but slightly less weighted.

---

## 4. Additional Considerations

### 4.1 Activity Decay
To account for over-engagement or unusually high activity, scores can be decayed by 10% if certain thresholds are exceeded:


Where the weights reflect the importance of each metric:

- w_P = 0.40 (Progress)  Most important metric; reflects student milestone completion.
- w_R = 0.25 (Responsiveness)  Measures timely support; important but secondary to
- w_E = 0.20 (Engagement)  Shows mentor involvement through meetings, code reviews, and messages.
- w_F = 0.15 (Feedback)  Represents student perception; weighted lower due to subjectivity and potential bias.

**Rationale:** Progress is most critical, followed by responsiveness. Engagement and feedback are still important but slightly less weighted.

---

## 4. Additional Considerations

### 4.1 Activity Decay
To account for over-engagement or unusually high activity, scores can be decayed by 10% if certain thresholds are exceeded:

**Rationale:** Avoids over-rewarding mentors with excessive activity that may not reflect quality.

### 4.2 Score Evolution Over Time
Combines current score with previous scores for stability:
M_new = (1 - a) * M_prev + a * M_curr
a = 0.3


**Rationale:** Ensures that scores are stable over time and small fluctuations do not drastically change rankings.

---

## 5. Assumptions
- All mentors have at least one student and one interaction.  
- Feedback ratings are on a 1–5 scale.  
- Response time is measured in hours.  

---

## 6. Workflow Diagram
CSV Files:
mentors.csv
students.csv
interactions.csv
feedbacks.csv
|
v
Load all data into memory
|
v
Compute raw scores for each mentor:
- P (Progress)
- R (Responsiveness)
- E (Engagement)
- F (Feedback)
|
v
Normalize scores (P_norm, E_norm, F_norm)
|
v
Apply weights and compute final Score
|
v
Apply Activity Decay (if thresholds met)
|
v
Update score with Score Evolution formula
|
v
Rank mentors by final Score
|
v
Save to mentor_scores.csv


---

## 7. Summary
This scoring system integrates multiple performance metrics, normalizes them, and applies a weighted formula to rank mentors fairly. By including decay and score evolution, the system accounts for both current performance and historical consistency, producing a balanced mentor ranking.