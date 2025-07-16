# VEGR512 Verifier for Google Electronic Returns (VGER) Version 1.5 SHA512 Edition
# Copyright (C) 2025  Benjamin Lord

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This program checks Letter.pdf and 12345678-20250101-1.zip archives provided by Google during legals service.
# SHA512 hash values within the PDF are compared to nested ZIPs contained within the primary ZIP.
# Standalone ZIP archives are autodetected and compared.
# Results are printed to screen and logged to 12345678-20250101-1.zip.txt
# Requires pypdf library for Python execution

# This software was designed to handle return archives in two formats known to the author on 7/16/2025.
# Variations made by Google outside of the two known formats will likely produce "mismatch or error" results
