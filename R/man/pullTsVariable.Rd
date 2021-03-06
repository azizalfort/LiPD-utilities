% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/lipdManipulation.R
\name{pullTsVariable}
\alias{pullTsVariable}
\title{pull variable out of TS object}
\usage{
pullTsVariable(TS, variable)
}
\arguments{
\item{TS}{a LiPD Timeseries object}

\item{variable}{the name of variable in a TS object}
}
\value{
a vector of the values, with NA representing instances without this variable.
}
\description{
pulls all instances of a single variable out of a TS
}
\seealso{
Other LiPD manipulation: 
\code{\link{pushTsVariable}()},
\code{\link{tidyTsOld}()},
\code{\link{tidyTs}()}
}
\concept{LiPD manipulation}
