# db/seeds.rb
puts "Seeding database..."

puts "Clearing existing data..."
Document.destroy_all
TimeOffRequest.destroy_all
Department.destroy_all
Employee.destroy_all
User.destroy_all

#
# 1. Create Users
#
puts "Creating Users..."
admin_user = User.create!(
  email:    'admin@example.com',
  password: 'admin123',
  role:     'admin'
)

regular_user = User.create!(
  email:    'user@example.com',
  password: 'user123',
  role:     'user'
)

#
# 2. Create Employees
#
puts "Creating Employees..."
admin_employee = Employee.create!(
  first_name: 'Admin',
  last_name:  'User',
  title:      'Manager',
  user:       admin_user
)

regular_employee = Employee.create!(
  first_name: 'Regular',
  last_name:  'User',
  title:      'Engineer',
  user:       regular_user
)

#
# 3. Create Departments
#
puts "Creating Departments..."
engineering = Department.create!(
  name:    'Engineering',
  manager: admin_employee
)

hr = Department.create!(
  name:    'Human Resources',
  manager: admin_employee
)

#
# 4. Create TimeOffRequests
#
puts "Creating Time Off Requests..."
request_admin = TimeOffRequest.create!(
  employee:   admin_employee,
  start_date: Date.today + 5.days,
  end_date:   Date.today + 8.days,
  reason:     'Admin holiday',
  status:     'pending'
)

request_user = TimeOffRequest.create!(
  employee:   regular_employee,
  start_date: Date.today + 10.days,
  end_date:   Date.today + 12.days,
  reason:     'Family event',
  status:     'pending'
)

puts "Seeding complete."
