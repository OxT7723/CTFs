class SessionsController < ApplicationController
  def new
    Rails.logger.info "SessionsController#new called"
  end

  def create
    Rails.logger.info "SessionsController#create called with params: #{params.inspect}"

    user = User.find_by(email: params[:email])
    if user&.authenticate(params[:password])
      Rails.logger.info "User #{user.email} authenticated successfully."

      session[:user_id] = user.id
      flash[:notice] = "Logged in successfully"
      redirect_to root_path
    else
      Rails.logger.info "Invalid login attempt for email: #{params[:email]}"
      flash[:alert] = "Invalid email or password"
      render :new, status: :unauthorized
    end
  end

  def destroy
    Rails.logger.info "SessionsController#destroy called for user_id #{session[:user_id]}"
    session.delete(:user_id)
    flash[:notice] = "Logged out"
    redirect_to login_path
  end
end
