class DashboardController < ApplicationController
  before_action :require_login

  def index
    @employee_count = Employee.count
    @department_count = Department.count

    if current_user.role == "manager" || current_user.role == "admin"
      @pending_requests = TimeOffRequest.where(status: "pending").count
    else
      @my_approved_requests = TimeOffRequest
                              .joins(:employee)
                              .where(employees: { user_id: current_user.id }, status: 'approved')
                              .count
    end
  end
end
