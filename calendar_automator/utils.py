def label2percentgoal(x):
  label_percent_goals={
    'p1': 80,
    'p2': 10,
    'p3': 5,
    'p4': 5,
    'service': 10,
    'literature': 10
  }
  if x in label_percent_goals:
    return label_percent_goals[x]
  else:
    return "N/A"

def label2name(x):
  labels = {
    'p1': "    Important &     Urgent",
    'p2': "    Important & Not Urgent",
    'p3': "Not Important & Urgent",
    'p4': "Not Important & Not Urgent",
  }
  if x in labels:
    return labels[x]
  else:
    return x.capitalize()

def task_labels(task):
  beginning = task.find("[")+1
  end = task.find("]")
  sub = task[beginning:end]
  
  if beginning > 0:
    labels = list(set(sub.split(",")))
  else:
    labels = []
  # import ipdb; ipdb.set_trace()
  if not('p1' in labels or 'p2' in labels or 'p3' in labels or 'p4' in labels):
    labels.append('p1')

  return labels



  # # ======================================================
  # # Want to print :
  # # Priority| Time | % Total Time
  # # ======================================================
  # # -----------------------
  # # first get time used for each
  # # -----------------------
  # label2length = collections.defaultdict(float)
  # total_scheduled = 0
  # for fulltask_name, length in fulltask2length.items():
  #   if fulltask_name in scheduling_events: continue
  #   labels = task_labels(fulltask_name)
  #   # import ipdb; ipdb.set_trace()
  #   for label in labels:
  #     label2length[label] += length

  #   total_scheduled += length


  # # -----------------------
  # # now print
  # # -----------------------
  # header = ["Label", "Time: %.1f/%.1f" % (total_scheduled, total_time), "Percent Scheduled", "Percent Total", "Goal"]
  # lines = []
  # for label, time in label2length.items():
  #   # if not label: continue

  #   label_name = label2name(label)
  #   name = f"{label_name}"
  #   time_percent_scheduled = 100*(time/total_scheduled)
  #   time_percent_total = 100*(time/total_time)
  #   line = [name, "%.1f" % time, "%2.f" % time_percent_scheduled, "%2.f" % time_percent_total, label2percentgoal(label)]
  #   lines.append(line)


  # print(term.olivedrab1("="*15 + " Scheduled Time Priority Distribtuon " + "="*15))
  # print(tabulate(lines, headers=header, tablefmt="pretty"))
  



