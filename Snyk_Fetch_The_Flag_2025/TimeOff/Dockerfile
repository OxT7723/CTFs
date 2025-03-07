FROM ruby:3.2

RUN apt-get update -qq && apt-get install -y nodejs
RUN mkdir /timeoff_app
WORKDIR /timeoff_app

COPY app/Gemfile app/Gemfile.lock ./
RUN bundle install

COPY app/ ./
COPY flag.txt /timeoff_app/flag.txt

RUN mkdir -p tmp/pids

RUN rails assets:precompile

EXPOSE 3000
CMD ["bash", "-c", "bundle exec rake db:consolidate_and_seed && bundle exec puma -C config/puma.rb"]
