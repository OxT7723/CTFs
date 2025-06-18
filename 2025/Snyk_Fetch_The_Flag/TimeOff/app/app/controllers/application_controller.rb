class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception

  # Simple method to fetch the currently logged-in user
  helper_method :current_user

  private

  def current_user
    @current_user ||= User.find_by(id: session[:user_id]) if session[:user_id]
  end

  def require_login
    unless current_user
      flash[:alert] = "You must be logged in to access this section."
      redirect_to login_path
    end
  end
end
