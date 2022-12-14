package io.gryteck.userservice.service

import io.gryteck.common.safeBody
import io.gryteck.user_service_api.UserInfoResponse
import io.gryteck.userservice.feign.BonusServiceApi
import io.gryteck.userservice.feign.TicketServiceApi
import io.gryteck.userservice.mapper.toPrivilegeShortInfo
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.reactive.asFlow
import org.springframework.stereotype.Service
import java.lang.Exception

@Service
class NetworkUserService(
    private val bonusServiceApi: BonusServiceApi,
    private val ticketServiceApi: TicketServiceApi
): UserService {
    override suspend fun getUserInfo(username: String): UserInfoResponse {
        val tickets = ticketServiceApi.getAllUserTickets(username).safeBody().asFlow().toList()
        val privilege = bonusServiceApi.getPrivilegeInfo(username).safeBody().asFlow().first()
            .toPrivilegeShortInfo()
        return UserInfoResponse(tickets = tickets, privilege = privilege)
    }
}