# clear what you've been experimenting with on 6/12 & 6/19
# ipython clear.py -- -s '6/12/18' -e '6/20/18' -v

dir=templates/msft_summer
# mkdir $dir

# copy tues, 5th to mon, 11th
week_day_file=$dir/week_day.yaml
# ipython read.py -- -s 6/5/18 -e 6/6/18 -f $week_day_file -v
# ipython put.py -- -s 6/11/18 -f $week_day_file -v -r 1

# copy tuesday - sunday (5-10) to tuesday - sunday (12-17)
# week_day_file=$dir/week_tues_sun.yaml
# ipython read.py -- -s 6/5/18 -e 6/11/18 -f $week_day_file -v
# ipython put.py -- -s 6/12/18 -f $week_day_file -v

##### TILING ########
# tile mon - sun (6/11-6/17) until 8/6-8/12 then clear sunday
# week_day_file=$dir/week_mon_sun.yaml
# ipython read.py -- -s 6/11/18 -e 6/18/18 -f $week_day_file
# ipython clear.py -- -s 6/18/18 -e 8/13/18 -v
# ipython put.py -- -s 6/18/18 -e 8/13/18 -f $week_day_file -r 7 -v
# ipython clear.py -- -s 8/12/18 -v


# # copy 6/12-6/17 to 6/5-6/10
# ipython replicate.py -- -bR 6/12 6/17 -rR 6/5 6/10 -c -v
# tile 6/11-6/17 every 7 days until 8/12
# ipython replicate.py -- -bR 6/11 6/17 -rR 6/18 8/12 -c -v

# copy 6/11 to monday, tuesday, thursday of 8/27 week
# week_day_file=$dir/week_day.yaml
# ipython read.py -- -s 6/11/18 -f $week_day_file -v
# ipython put.py -- -s 8/27/18 -f $week_day_file -v -c
# ipython put.py -- -s 8/28/18 -f $week_day_file -v -c
# ipython put.py -- -s 8/30/18 -f $week_day_file -v -c

# ------ shift 6/11 by 1 hour
# ipython read.py -- -s 6/11/18
# ipython shift.py -- -s 6/11/18 -m 60 -v
# ------ copy to rest of week
# ipython replicate.py -- -bR 6/11 6/12 -rR 6/12 6/16 -v -c
# ------ copy to rest of semester
# ipython replicate.py -- -bR 6/11 6/18 -rR 6/18 8/13 -v -c



# ipython read.py -- -s 6/23/18 -f templates/6_23.yaml -v
# ipython read.py -- -s 6/24/18 -f templates/6_24.yaml -v

# echo
# echo "putting 6/23"
# ipython put.py -- -s 6/23/18 -f templates/6_24.yaml -v -c

# echo
# echo "putting 6/24"
# ipython put.py -- -s 6/24/18 -f templates/6_23.yaml -v -c

# ipython clear.py -- -s 8/4 -e 8/6 -v


# copy 6/25 to monday, tues & 6/26 to wed, thurs, fri
# day_25=$dir/6_25.yaml
# day_26=$dir/6_26.yaml
# ipython read.py -- -s 6/25/18 -f $day_25 -v
# ipython read.py -- -s 6/26/18 -f $day_26 -v

# copy
ipython replicate.py -- -bR 7/2 7/9 -rR 7/9 7/16 -v -c
ipython replicate.py -- -bR 7/2 7/5 -rR 7/16 7/20 -v -c
ipython replicate.py -- -bR 7/2 7/9 -rR 7/23 8/6 -v -c
ipython replicate.py -- -bR 7/2 7/5 -rR 8/27 8/31 -v -c
# ipython put.py -- -s 7/4 -e 7/7 -r 1 -f $day_26 -v -c

# calculate available time
ipython available_time.py -- -f tasks/msft_summer.yaml -e 8/31



