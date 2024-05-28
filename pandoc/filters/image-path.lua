function Image(img)
	if img.src:sub(1, 1) == '/' then
		local gitRoot = io.popen('git rev-parse --show-toplevel 2>/dev/null'):read("*l")
		if gitRoot == nil then
			img.src = '.' .. img.src
		else
			img.src = gitRoot .. img.src
		end
	end
	return img
end
