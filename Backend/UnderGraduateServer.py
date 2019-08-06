import csv
import urllib.request
import random
import heapq
from flask import Flask, render_template, escape, request, redirect
import pandas as pd

from enum import Enum

class UserProfile:
  sat_score =0
  max_tuition =0
  def __init__(self, sat_score, max_tuition):
      self.sat_score = sat_score
      self.max_tuition = max_tuition


class CollegeInfo: 
  rank =0
  city =''
  state =''
  tuition =0
  sat =0
  accept_rate =0
  debt =0
  male_ratio =0
  def __init__(self, rank, city, state, tuition, sat, accept_rate, debt, male_ratio):
      self.rank = rank
      self.city = city
      self.state =state
      self.tuition = tuition
      self.sat =sat
      self.accept_rate =accept_rate
      self.debt =debt
      self.male_ratio =male_ratio  
  
  def ToString(self) :
      return self.city + '\t' + self.state +'\t' + str(self.rank) +'\t' + str(self.tuition) +'\t' + str(self.sat) +'\t' + str(self.accept_rate) +'\t' + str(self.debt) +'\t' + str(self.male_ratio)

  def ToStringWithName(self) :
      return 'city:' + self.city + '\tstate:' + self.state +'\trank:' + str(self.rank) +'\ttuition:' + str(self.tuition) +'\tsat:' + str(self.sat) +'\tAC:' + str(self.accept_rate) +'\tdebt:' + str(self.debt) +'\tMal:' + str(self.male_ratio)


def extract_ranking_field(filename, column_names):
  reader = open(filename)
  input_file = csv.DictReader(reader)
  ret ={}
  for key in column_names:
    ret[key]=[]
  for row in input_file:   
    for key in column_names:
       if key in row.keys():
         ret[key].append(row[key])
  reader.close()
  return ret
  
def process_input() :

  while True:    
    input2_tmp = request.args.get("sat")
    try:
      input2 =float(input2_tmp)
    except Exception as ex:
      continue
    break
  while True:    
    input3_tmp = request.args.get("tution")
    try:
      input3 =float(input3_tmp)
    except Exception as ex:
      continue
    break
  return UserProfile(input2, input3)

def UniversityRank():
  url = "http://www.4icu.org/us/"
  handle = urllib.request.urlopen(url)
  html =  handle.read()
  html=html.decode("utf8")
  result ={}
  location =0
  rank =0
  while True:
    try:
      location1 = html.index('.htm">', location)
      print(location1)
      location2 =html.index('</a>', location1)
      print(location2)
      result[html[(location1 + len('.htm">')): location2]] =rank
      rank =rank +1
      location =location2 +1
    except Exception as ex:
      break
  return result

def ProcessFinalData(user_data, college_rank):
   size =len(user_data['INSTNM'])
   result ={}
   for i in range(size):
      name =user_data['INSTNM'][i]
      if name not in college_rank:
         continue
      rank =college_rank[name]
      city =user_data['CITY'][i]
      state =user_data['STABBR'][i]
      try:
        tuition =float(user_data['TUITIONFEE_OUT'][i])
        sat =float(user_data['SAT_AVG_ALL'][i])
        accept_rate =float(user_data['ADM_RATE_ALL'][i])
        tuition =float(user_data['TUITIONFEE_OUT'][i])
        debt =float(user_data['DEBT_MDN_SUPP'][i])
        male_ratio =float(user_data['UGDS_MEN'][i])
        result[name] =CollegeInfo(rank, city, state, tuition, sat, accept_rate, debt, male_ratio)
      except Exception as ex:
        pass
   return result

def saveDataToFile(final_data) :

   f = open('cleanData.tsv', 'w')
   #(pd.DataFrame.from_dict(data=final_data, orient='columns')
   # .to_csv('final_data.csv', header=False))
   for (k, v) in final_data.items():
     f.write(k + '\t' + v.ToString()+'\n')
   f.close()


def FilterCollege(user_profile, data):
   result ={}
   for (k, v) in data.items():
      if user_profile.sat_score >= v.sat and user_profile.max_tuition >= v.tuition:
          result[k] =v
   return result

def NormalizeData(data) :

  norm_max =max(data)
  norm_min =min(data)
  
  result =[]
  for i in data:
    if (norm_max ==norm_min):
      result.append(1)
    else:
      result.append((i - norm_min)*1.0 /(norm_max -norm_min))
  return result

def GetTopN(data, score, N):
  Top = sorted(score.items(), key=lambda x:-x[1])[:5]
  return Top

def Recommendations(data):
  names =[]
  sats =[]  
  tuitions =[]
  ranks =[]
  accept_rates =[]

  for (k, v) in data.items():
     names.append(k)
     tuitions.append(v.tuition)
     sats.append(v.sat)
     accept_rates.append(v.accept_rate)
     ranks.append(v.rank)
  tuitions =NormalizeData(tuitions)
  ranks =NormalizeData(ranks)
  sats =NormalizeData(sats)
  
  score={}
  for i in range(len(names)):
    score[names[i]] =0.15 * (1 - tuitions[i]) + 0.4* (1 -sats[i]) + 0.35*accept_rates[i] + 0.2*(1-ranks[i])
  recommendation = GetTopN(data, score, 5)
  return recommendation


  
   
def main():
   print("loading Recent University data")
  
   user_data =extract_ranking_field('../WebScraped_data/csv/MERGED2016_17_PP.csv', ['INSTNM', 'CITY', 'STABBR' ,'TUITIONFEE_OUT',  'SAT_AVG_ALL', 'ADM_RATE_ALL', 'DEBT_MDN_SUPP', 'UGDS_MEN'])
   college_rank = UniversityRank()
   final_data = ProcessFinalData(user_data, college_rank)
   saveDataToFile(final_data)

   while True:
      user_profile = process_input()
      filter_data =FilterCollege(user_profile, final_data) 

      if len(filter_data) ==0:
          continue

      else:
        result = Recommendations(filter_data)

      print("Result in college",result)  
      return result 

if __name__ == "__main__": 
    main()
