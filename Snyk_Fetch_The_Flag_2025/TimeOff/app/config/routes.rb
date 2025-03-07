Rails.application.routes.draw do
  root 'dashboard#index'

  get  '/login',  to: 'sessions#new'
  post '/login',  to: 'sessions#create'
  delete '/logout', to: 'sessions#destroy'

  resources :time_off_requests, only: [:index, :new, :create, :show]

  get '/manager/time_off_requests', to: 'time_off_requests#manager_index', as: 'manager_time_off_requests'
  patch '/manager/time_off_requests/:id/approve', to: 'time_off_requests#approve', as: 'approve_time_off_request'
  patch '/manager/time_off_requests/:id/deny',    to: 'time_off_requests#deny',    as: 'deny_time_off_request'

  resources :employees
  resources :departments
  resources :documents, only: [] do
    member do
      get :download
    end
  end
  

end
