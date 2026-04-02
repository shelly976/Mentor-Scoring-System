import pandas as pd
import math
from datetime import datetime

mentorfile='./data/mentors.csv'
feedbackfile='./data/feedbacks.csv'
studentsfile='./data/students.csv'
interactionfile='./data/interactions.csv'
mentorscoresfile='./output/mentor_scores.csv'

array=[]
array1=[]
array2=[]

df= pd.read_csv(mentorfile, sep=',')
Index=0
pd.DataFrame(columns=['MentorID','Name','Score']).to_csv(
    mentorscoresfile,index=False,header=True
)
lk=pd.read_csv(mentorscoresfile,sep=',')

# getting value of average students under mentors to normalize to each P,R,E,F

Nstudents=0
Nmentors=0
for index,row in df.iterrows():
    Nmentors+=1
    mentorID=row['MentorID']

    f=pd.read_csv(studentsfile, sep=',')
    mentorprojects=row['Projects'].split(',')
    for i in mentorprojects:
        rows = f[f['ProjectID']==i]
        for k,l in rows.iterrows():
            Nstudents=Nstudents+1
average=Nstudents/Nmentors

# ------------------------------------------------------------


for index,row in df.iterrows():
    mentorID=row['MentorID']
    mentorname=row['Name']
    if lk.empty:
        Mt=0
    else:
        sortedrow=lk[lk['MentorID']==mentorID]
        Mt=sortedrow['Score']
    mentorprojects=row['Projects'].split(',')
    # print(mentorprojects)

#    GET student progress score for each mentor
    #finding max and min average progress student score of mentors for normalizations
    if mentorID=='M001':
        for index,row in df.iterrows():
            mentorID2=row['MentorID']

            mentorprojects1=row['Projects'].split(',')
            f=pd.read_csv(studentsfile, sep=',')
            s=0
            q=0
            for i in mentorprojects1:
                rows = f[f['ProjectID']==i]
                for k,l in rows.iterrows():
                    q=q+1
                    s+=l['MilestonesCompleted']/l['TotalMilestones']
            if q==0:
                P=0
            else:
                P=s/q
            array2.append(P)
    #---------------------------------------------------------------------
    Max3=max(array2)
    Min3=min(array2)

    f=pd.read_csv(studentsfile, sep=',')
    s=0
    q=0
    for i in mentorprojects:
        rows = f[f['ProjectID']==i]
        for k,l in rows.iterrows():
            q=q+1
            s+=l['MilestonesCompleted']/l['TotalMilestones']
    if q==0:
        P=0
    else:
        P=s/q
    P=(P-Min3)/(Max3-Min3)
  
#   Responsiveness Score (R).

    r=pd.read_csv(interactionfile,sep=',')
    rows = r[r['MentorID']==mentorID]
    n=0
    tavg=0
    for index,row in rows.iterrows():
        n=n+1
        tavg+=row['AvgResponseTime']
    if n==0:
        R=0
    else:
        tavg /=n
        #0.1 is Strictness
        h=0.1
        R=math.exp(-h*tavg)
        
    # print(R)
#   Engagement Score (E).
     
     # finding max engangement score and minimum for normalization

    if mentorID=='M001':
        for index,row in df.iterrows():
            mentorID1=row['MentorID']
            rr=pd.read_csv(interactionfile,sep=',')
            rows = rr[rr['MentorID']==mentorID1]
            nn=0
            m=0
            r=0
            i=0
            for index,row in rows.iterrows():
                nn=nn+1
                m+=row['Meetings']
                r+=row['CodeReviews']
                i+=row['Messages']
            if nn==0:
                M=0
                R1=0
                I=0
            else:
                M = m/(nn)
                R1 = r/(nn)
                I = i/(nn)

            E = M*0.4+R1*0.4+I*0.2
            array.append(E)
    #--------------------------------------------------------

    Max=max(array)
    Min=min(array)

    for index,row in df.iterrows():
        mentorID11=row['MentorID']
        rr=pd.read_csv(interactionfile,sep=',')
        rows = rr[rr['MentorID']==mentorID11]
        nn=0
        m=0
        r=0
        i=0
        for index,row in rows.iterrows():
            nn=nn+1
            m+=row['Meetings']
            r+=row['CodeReviews']
            i+=row['Messages']
        if nn==0:
            M=0
            R1=0
            I=0
        else:
            M = m/(nn)
            R1 = r/(nn)
            I = i/(nn)

        Etemp = M*0.4+R1*0.4+I*0.2
        E=(Etemp-Min)/(Max-Min)



#   Mentee Feedback Score (F).
    # finding min max feedback average for each student 
    if mentorID =='M001':
        print('hello')
        d = pd.read_csv(feedbackfile,sep=',')
        df= pd.read_csv(mentorfile, sep=',')
        for index,roww in df.iterrows():
            mentorID2=roww['MentorID']
            f=d[d['MentorID']==mentorID2]
            ff=0
            nnn=0
            for index,rowww in f.iterrows():
                nnn+=1
                Rating=rowww['Rating']
                #Detecting Unfair Feedback:
                if Rating<1.5:
                    ff+=2
                elif Rating>4.5:
                    ff+=4
                else:
                    ff+=Rating
            if nnn==0:
                F=0
            else:
                F=ff/nnn
            array1.append(F)
    Max1=max(array1)
    Min1=min(array1)
    #--------------------------------------------------
    

    d = pd.read_csv(feedbackfile,sep=',')
    f=d[d['MentorID']==mentorID]
    ff=0
    nnn=0
    for index,row in f.iterrows():
        nnn+=1
        Rating=row['Rating']
        #Detecting Unfair Feedback:
        if Rating<1.5:
            ff+=1.5
        elif Rating>4.5:
            ff+=4
        else:
            ff+=Rating
    if nnn==0:
        F=0
    else:
        F=ff/nnn
    F=(F-Min1)/(Max1-Min1)
    
    Mcurr1 = P*0.40+R*0.25 + E*0.2+0.15*F
    
#   1.2.3 Activity Decay(where 6 comes from E=3meetings*0.4+6codereviews*0.4+10messages*0.2)

    dc=0.1  # decreading the M score by 10 percentage on decaying.
    if M>=3 and R1>=6 and I>=10:
        Mcurr=Mcurr1*(1-dc)
    else:
        Mcurr= Mcurr1
    
#1.2.2 Score Evolution Over Time(70% for current Mvalue and 30% for previous one)

    a=0.3
    Mnew=Mt*(1-a)+Mcurr*a
    Index+=1
    
    sd = pd.read_csv(mentorscoresfile,sep=',')
    sdrow=sd[sd['MentorID']==mentorID]

    if sdrow.empty:
        row=pd.DataFrame([[mentorID,mentorname,Mnew]],columns=['MentorID','Name','Score'])
        row.to_csv(mentorscoresfile,mode='a',index=False,header=False)
    else :
      sd.loc[sd['MentorID']==mentorID,'Score']=M
      sd.to_csv(mentorscoresfile,index=False)

sort = pd.read_csv(mentorscoresfile)
sorted=sort.sort_values(by='Score',ascending=False)
sorted.to_csv(mentorscoresfile,index=False)
sorted.insert(0,'Rank',range(1,len(sorted)+1))
sorted.to_csv(mentorscoresfile, index=False)

#printing formated table
pft=pd.read_csv(mentorscoresfile,sep=',')
print('Rank','MentorID',"    ",'Name',"    ",'M(m)')
for index,row in pft.iterrows():
    print(row['Rank'],row['MentorID'],"    ",row['Name'],"    ",row['Score'])