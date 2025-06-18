# app/controllers/time_off_requests_controller.rb
class TimeOffRequestsController < ApplicationController
  before_action :require_login
  before_action :require_manager, only: [:manager_index, :approve, :deny]

  def index
    @employee = Employee.find_by(user_id: current_user.id)
    @time_off_requests = @employee.time_off_requests.order(created_at: :desc)
  end

  def new
    @time_off_request = TimeOffRequest.new
  end

  def create
  @employee = Employee.find_by(user_id: current_user.id)
  @time_off_request = @employee.time_off_requests.build(time_off_request_params)

  if params[:doc]
    uploaded_file = params[:doc][:file]
    if uploaded_file
      storage_directory = Rails.root.join("public", "uploads")
      FileUtils.mkdir_p(storage_directory) unless Dir.exist?(storage_directory)
      storage_path = storage_directory.join(uploaded_file.original_filename)

      Rails.logger.info "Saving uploaded file to: #{storage_path}"

      File.open(storage_path, "wb") do |file|
        file.write(uploaded_file.read)
      end

      doc = Document.new(
        name: params[:doc][:file_name],
        file_path: uploaded_file.original_filename
      )
      doc.time_off_request = @time_off_request
      doc.save
    end
  end

  if @time_off_request.save
    flash[:notice] = "Time off request submitted successfully."
    redirect_to @time_off_request
  else
    flash[:alert] = @time_off_request.errors.full_messages.to_sentence
    render :new, status: :unprocessable_entity
  end
end


  def show
    @time_off_request = TimeOffRequest.find(params[:id])
  end

  def manager_index
    @time_off_requests = TimeOffRequest.includes(:employee, :document).order(status: :asc, created_at: :desc)
  end

  def approve
    request = TimeOffRequest.find(params[:id])
    request.update(status: 'approved')
    flash[:notice] = "Request approved."
    redirect_to manager_time_off_requests_path
  end

  def deny
    request = TimeOffRequest.find(params[:id])
    request.update(status: 'denied')
    flash[:notice] = "Request denied."
    redirect_to manager_time_off_requests_path
  end

  private

  def time_off_request_params
    params.require(:time_off_request).permit(:start_date, :end_date, :reason)
  end

  def require_manager
    unless current_user&.role.in?(%w[manager admin])
      redirect_to root_path, alert: "Not authorized."
    end
  end
end

