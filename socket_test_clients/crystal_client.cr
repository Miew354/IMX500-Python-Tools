require "socket"
require "json"

category = "evil_cat" # category to trigger on
confidence = 0.8 # confidence threshold

def colorize(text, color_code)
  "\e[#{color_code}m#{text}\e[0m"
end

def green(text)
  colorize(text, 32)
end

def red(text)
  colorize(text, 31)
end

UNIXSocket.open("/tmp/detections.sock") do |sock|
  loop do
    data = sock.gets
    break unless data
    begin
      parsed_data = JSON.parse(data)
      detections = parsed_data.as_a rescue [parsed_data]
      detections.each do |detection|
        detection_confidence = detection["confidence"].as_f * 100
        if detection["category"].as_s == category && detection_confidence >= confidence * 100
          puts green("parameters met: category=#{detection["category"]}, confidence=#{detection_confidence.round(2)}%")
        else
          puts red("parameters not met: category=#{detection["category"]}, confidence=#{detection_confidence.round(2)}%")
        end
      end
    rescue ex : JSON::ParseException
      puts "Failed to parse JSON: #{ex.message}"
    rescue ex : Exception
      puts "Unexpected error: #{ex.message}"
    end
  end
end